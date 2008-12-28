﻿"""
Authorisation related functions.

The actions a User is authorised to perform are dependent on their reputation
and superuser status.
"""
VOTE_UP                   = 15
FLAG_OFFENSIVE            = 15
POST_IMAGES               = 15
LEAVE_COMMENTS            = 50
VOTE_DOWN                 = 100
CLOSE_OWN_QUESTIONS       = 250
RETAG_OTHER_QUESTIONS     = 500
EDIT_COMMUNITY_WIKI_POSTS = 750
EDIT_OTHER_POSTS          = 2000
DELETE_COMMENTS           = 2000
VIEW_OFFENSIVE_FLAGS      = 2000
DISABLE_URL_NOFOLLOW      = 2000
CLOSE_OTHER_QUESTIONS     = 3000
LOCK_POSTS                = 4000

VOTE_RULES = {
    'scope_votes_per_user_per_day' : 30, # how many votes of one user has everyday
    'scope_flags_per_user_per_day' : 5,  # how many times user can flag posts everyday
    'scope_warn_votes_left' : 10,        # start when to warn user how many votes left
    'scope_deny_unvote_days' : 1,        # if 1 days passed, user can't cancel votes.
}

REPUTATION_RULES = {
    'initial_score'                       : 1,
    'scope_per_day_by_upvotes'            : 200,
    'gain_by_upvoted'                     : 10,
    'gain_by_answer_accepted'             : 15,
    'gain_by_accepting_answer'            : 2,
    'gain_by_downvote_canceled'           : 2,
    'gain_by_canceling_downvote'          : 1,
    'lose_by_downvoted'                   : -2,
    'lose_by_flagged'                     : -2,
    'lose_by_downvoting'                  : -1,
    'lose_by_flagged_lastrevision_3_times': -30,
    'lose_by_flagged_lastrevision_5_times': -100,
    'lost_by_upvote_canceled'             : -10,
}
def can_vote_up(user):
    """Determines if a User can vote Questions and Answers up."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_UP or
        user.is_superuser)

def can_flag_offensive(user):
    """Determines if a User can flag Questions and Answers as offensive."""
    return user.is_authenticated() and (
        user.reputation >= FLAG_OFFENSIVE or
        user.is_superuser)

def can_add_comments(user):
    """Determines if a User can add comments to Questions and Answers."""
    return user.is_authenticated() and (
        user.reputation >= LEAVE_COMMENTS or
        user.is_superuser)

def can_vote_down(user):
    """Determines if a User can vote Questions and Answers down."""
    return user.is_authenticated() and (
        user.reputation >= VOTE_DOWN or
        user.is_superuser)

def can_retag_questions(user):
    """Determines if a User can retag Questions."""
    return user.is_authenticated() and (
        RETAG_OTHER_QUESTIONS <= user.reputation < EDIT_OTHER_POSTS)

def can_edit_post(user, post):
    """Determines if a User can edit the given Question or Answer."""
    return user.is_authenticated() and (
        user.id == post.author_id or
        (post.wiki and user.reputation >= EDIT_COMMUNITY_WIKI_POSTS) or
        user.reputation >= EDIT_OTHER_POSTS or
        user.is_superuser)

def can_delete_comment(user, comment):
    """Determines if a User can delete the given Comment."""
    return user.is_authenticated() and (
        user.id == comment.user_id or
        user.reputation >= DELETE_COMMENTS or
        user.is_superuser)

def can_view_offensive_flags(user):
    """Determines if a User can view offensive flag counts."""
    return user.is_authenticated() and (
        user.reputation >= VIEW_OFFENSIVE_FLAGS or
        user.is_superuser)

def can_close_question(user, question):
    """Determines if a User can close the given Question."""
    return user.is_authenticated() and (
        (user.id == question.author_id and
         user.reputation >= CLOSE_OWN_QUESTIONS) or
        user.reputation >= CLOSE_OTHER_QUESTIONS or
        user.is_superuser)

def can_lock_posts(user):
    """Determines if a User can lock Questions or Answers."""
    return user.is_authenticated() and (
        user.reputation >= LOCK_POSTS or
        user.is_superuser)

def can_follow_url(user):
    """Determines if the URL link can be followed by Google search engine."""
    return user.reputation >= DISABLE_URL_NOFOLLOW 

def can_accept_answer(user, question, answer):
    return (user.is_authenticated() and 
        question.author != answer.author and
        question.author == user) or user.is_superuser
    