import json
from itertools import chain
from random import shuffle

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError
from django.views.generic import CreateView, DetailView, ListView, UpdateView

from nablapps.accounts.models import NablaUser

from .forms import AlternativeFormset
from .models import (
    Alternative,
    DuplicatePriorities,
    HoleInBallotError,
    UserAlreadyVoted,
    UserNotEligible,
    Voting,
    VotingDeactive,
    VotingEvent,
)


####################
### Admin views ####
####################
def voting_to_JSON(voting):
    json = {}
    json["pk"] = voting.pk
    json["title"] = voting.title
    json["active"] = voting.is_active
    json["num_voted"] = voting.get_total_votes()
    json["created_by"] = getattr(voting.created_by, "username", "Admin (aka unknown)")
    json["url"] = reverse("voting-detail", kwargs={"pk": voting.pk})
    json["alternatives"] = {
        a.pk: {
            "pk": a.pk,
            "text": a.text,
            "votes": a.votes,
            "percentage": a.get_vote_percentage(),
        }
        for a in voting.alternatives.all()
    }
    return json


# Todo fix permissions
def register_attendance(request, event_pk, user_pk):
    """Check in/out user from a voting event.
    Verify that the user i eligable, and then perform the checkin.
    Return a status.

    GET paramters:
      action: String - one of 'toggle', 'in', 'out', 'nothing'. Default: 'toggle'

    Response:
      Json with the currently attending users."""

    try:
        event = VotingEvent.objects.get(pk=event_pk)
        user = NablaUser.objects.get(pk=user_pk)
    except VotingEvent.DoesNotExist:
        reason = "Event not found"
    except NablaUser.DoesNotExist:
        reason = "User not found"
    else:
        reason = None
    finally:
        if reason is not None:
            return JsonResponse(
                {
                    "status": "failure",
                    "reason": reason,
                    "user": None,
                    "inout": None,
                    "currently_checked_in": None,
                }
            )

    actions = {
        "toggle": event.toggle_check_in_user,
        "in": event.check_in_user,
        "out": event.check_out_user,
        "nothing": lambda user: None,
    }

    try:
        action = actions[request.GET.get("action", "toggle")]
        action(user)
    except KeyError:
        status = "failure"
        reason = (
            f"Invalid action '{request.GET['action']}'. Must be one of {actions.keys}"
        )
    except UserNotEligible:
        status = "failure"
        reason = "User is not eligible for this event"
    else:
        status = "success"
        reason = None

    return JsonResponse(
        {
            "status": status,
            "reason": reason,
            "user": user.username,
            "inout": event.user_checked_in(user),
            "currently_checked_in": [
                user.username for user in event.checked_in_users.all()
            ],
        }
    )


def register_attendance_card(request, event_pk, rfid_number):
    """Register attendance using card as identifyer"""
    user = NablaUser.objects.get_from_rfid(rfid_number)
    if user is not None:
        return register_attendance(request, event_pk, user.pk)
    else:
        return JsonResponse(
            {
                "status": "failure",
                "reason": "Unknown card",
                "user": None,
                "inout": None,
                "currently_checked_in": None,
            }
        )


def register_attendance_username(request, event_pk, username):
    """Register attendance using username as identifyer"""
    try:
        user = NablaUser.objects.get(username=username)
    except:  # noqa: E722 TODO specify
        return JsonResponse(
            {
                "status": "failure",
                "reason": f"Unknown username '{username}'",
                "user": None,
                "inout": None,
                "currently_checked_in": None,
            }
        )
    else:
        return register_attendance(request, event_pk, user.pk)


class RegisterAttendanceView(DetailView):
    model = VotingEvent
    template_name = "vote/register_attendance.html"


class VotingListJSONView(DetailView):
    """Could possibly do this function based"""

    permission_required = ("vote.vote_admin", "vote.vote_inspector")
    model = VotingEvent

    def get(self, request, *args, **kwargs):
        votings = self.get_object().votings.all()
        return JsonResponse(
            {"votings": {voting.pk: voting_to_JSON(voting) for voting in votings}}
        )

    def post(self, request, *args, **kwargs):
        votings = self.get_object().votings.all()
        data = json.loads(request.body)
        # NOTE: there are two pk
        # data.pk is the POST data referring to a voting
        # kwargs.pk is the GET data referring to the voting event of the view.
        to_change = votings.get(pk=data.get("pk"))
        to_change.is_active = data.get("active")
        to_change.save()
        return JsonResponse(
            {"votings": {voting.pk: voting_to_JSON(voting) for voting in votings}}
        )


class VotingEventList(PermissionRequiredMixin, ListView):
    permission_required = ("vote.vote_admin", "vote.vote_inspector")
    model = VotingEvent
    template_name = "vote/voting_event_list.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False


class VotingList(PermissionRequiredMixin, DetailView):
    """List of all votings in a voting event"""

    permission_required = ("vote.vote_admin", "vote.vote_inspector")
    model = VotingEvent
    template_name = "vote/voting_list.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = self.request.user.has_perm("vote.vote_admin")
        return context


class CreateVoting(PermissionRequiredMixin, CreateView):
    """View for creating new votings"""

    permission_required = "vote.vote_admin"
    template_name = "vote/voting_form.html"
    model = Voting
    fields = ["event", "title", "num_winners", "description"]

    def get_initial(self):
        event_id = self.kwargs["pk"]
        event = get_object_or_404(VotingEvent, pk=event_id)
        return {
            "event": event,
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        event_id = self.kwargs["pk"]
        context["event_id"] = event_id
        if self.request.POST:
            context["alternatives"] = AlternativeFormset(self.request.POST)
        else:
            context["alternatives"] = AlternativeFormset()
        return context

    def form_valid(self, form, **kwargs):
        """Called if all forms are valid. Creates voting and associated alternatives"""
        context = self.get_context_data()
        alternatives = context["alternatives"]
        event_id = self.kwargs["pk"]
        with transaction.atomic():
            self.object = form.save()
            if alternatives.is_valid():
                alternatives.instance = self.object
                event_id = alternatives.instance.event.pk
                alternatives.save()
        return redirect("voting-list", pk=event_id)
        return super().form_valid(form)


class VotingEdit(PermissionRequiredMixin, UpdateView):
    permission_required = "vote.vote_admin"
    model = Voting
    template_name = "vote/edit_voting.html"
    fields = ["event", "title", "description"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["alternatives"] = AlternativeFormset(self.request.POST)
        else:
            context["alternatives"] = AlternativeFormset()
        return context

    def form_valid(self, form, **kwargs):
        """Called if all forms are valid. Creates voting and associated alternatives"""
        if self.object.get_total_votes() == 0:
            context = self.get_context_data()
            alternatives = context["alternatives"]
            with transaction.atomic():
                self.object = form.save()
                if alternatives.is_valid():
                    alternatives.instance = self.object
                    alternatives.save()
            return redirect("voting-detail", pk=self.kwargs["pk"])
        else:
            messages.error(
                self.request,
                "OBS! Denne avstemningen har allerede blitt stemt på, endring ikke gyldig",
            )
            return redirect("voting-detail", pk=self.kwargs["pk"])


class VotingDetail(PermissionRequiredMixin, DetailView):
    """Display details such as alternatives and results"""

    permission_required = ("vote.vote_admin", "vote.vote_inspector")
    model = Voting
    template_name = "vote/voting_detail.html"

    def has_permission(self):
        perms = self.get_permission_required()
        for perm in perms:
            if self.request.user.has_perm(perm):
                return True
        return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_admin"] = self.request.user.has_perm("vote.vote_admin")

        if self.request.method == "POST":
            context["winners"] = self.object.get_multi_winner_result()
            print(self.object.get_multi_winner_result())
        else:
            self.object.multi_winnner_initial_dist()
        if self.object.num_winners > 1:
            context["quota"] = (
                int(self.object.get_total_votes() / (self.object.num_winners + 1)) + 1
            )
        return context

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def get_multi_winner_result(request):
    pass


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def activate_voting(request, pk, redirect_to):
    """Open voting"""
    voting = Voting.objects.get(pk=pk)
    voting.is_active = True
    voting.save()
    return redirect(redirect_to)


@login_required
@permission_required("vote.vote_admin", raise_exception=True)
def deactivate_voting(request, pk, redirect_to):
    """Close voting"""
    voting = Voting.objects.get(pk=pk)
    voting.is_active = False
    voting.save()
    return redirect(redirect_to)


###########################################
### Non admin views, only login required ###
###########################################


class ActiveVotingList(LoginRequiredMixin, ListView):
    """Display list of active votings"""

    model = Voting
    template_name = "vote/active_voting_list.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        admin_rights = ["vote.vote_admin", "vote.vote_inspector"]
        context["admin_rights"] = any(
            [self.request.user.has_perm(right) for right in admin_rights]
        )
        return context

    def get_queryset(self):
        all_user_votings = self.model.objects.exclude(is_active=False).filter(
            event__eligible_group=None
        )
        user_group_votings = self.model.objects.exclude(is_active=False).filter(
            event__eligible_group__in=self.request.user.groups.all()
        )
        return chain(all_user_votings, user_group_votings)


class Vote(LoginRequiredMixin, DetailView):
    """
    Display alternatives and lets users vote

    The form for voting is a little shabby(TM),
    probably smoother with formset. Didn't want to bother with big rewrite,
    so leaving that for future-improvement(TM) :^)

    The creation of the Ballot (container and entries) can probably also be
    written in a much nicer way. I think ultimately if all votations in the future will
    be using STV, then this view as a CreateView together with a formset for the
    priorities/alternatives is probably nice.

    Disclaimer: possible misuse of docstring
    Disclaimer2: possible misuse of the (TM) joke
    """

    model = Voting
    template_name = "vote/voting_vote.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        alternatives = self.object.alternatives.all()
        alternatives = [alt for alt in alternatives]
        shuffle(alternatives)
        context["randomized_alternatives"] = alternatives
        context["has_voted"] = self.object.user_already_voted(self.request.user)
        context["priorities"] = [
            i for i in range(1, self.object.get_num_alternatives() + 1)
        ]
        return context

    def post(self, request, **kwargs):
        """Submit a vote from chosen alternative"""
        voting_id = kwargs["pk"]
        voting = get_object_or_404(Voting, pk=voting_id)

        if voting.num_winners > 1:
            # Single transferable vote
            # Get list/dictonary of alternatives and priorities
            try:
                priorities = [i for i in range(1, voting.get_num_alternatives() + 1)]
                # ballot : {pri#:alternative.pk}
                ballot_dict = {}
                for pri in priorities:
                    try:
                        ballot_dict[pri] = request.POST["priority" + str(pri)]
                        if pri > 1:
                            if ballot_dict[pri - 1] is None:
                                raise HoleInBallotError("Hole in ballot")
                    except MultiValueDictKeyError:
                        ballot_dict[pri] = None
                    except HoleInBallotError:
                        messages.warning(
                            request, "Ikke tillatt med hull i stemmeseddelen"
                        )
                        return redirect("voting-vote", pk=voting_id)
                ballot_dict = {
                    pri: v for pri, v in ballot_dict.items() if v is not None
                }
                voting.submit_stv_votes(request.user, ballot_dict)
            except UserAlreadyVoted:
                messages.error(request, "Du har allerede stemt i denne avstemningen!")
            except VotingDeactive:
                messages.error(
                    request, "Denne avstemningen er ikke lenger åpen for stemming!"
                )
            except DuplicatePriorities:
                messages.warning(
                    request, "Du kan ikke velge samme kandidat flere ganger!"
                )
                return redirect("voting-vote", pk=voting_id)
            else:
                messages.success(
                    request, f"Suksess! Du har stemt i avstemningen {voting.title}"
                )
        else:
            # Normal voting, first past the post(?)
            try:
                alternative = voting.alternatives.get(pk=request.POST["alternative"])
                alternative.add_vote(request.user)
            except (KeyError, Alternative.DoesNotExist):
                messages.warning(request, "Du har ikke valgt et alternativ.")
                return redirect("voting-vote", pk=voting_id)
            except UserAlreadyVoted:
                messages.error(request, "Du har allerede stemt i denne avstemningen!")
            except VotingDeactive:
                messages.error(
                    request, "Denne avstemningen er ikke lenger åpen for stemming!"
                )
            else:
                messages.success(
                    request, f"Suksess! Du har stemt i avstemningen {voting.title}"
                )
        return redirect("active-voting-list")
