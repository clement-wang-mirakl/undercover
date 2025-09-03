#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Uncover game

# Compared to the standard game:
# 1. The list of words is constrained.
# 2. The order of players is random at each round.
# 3. The votes are secret.

# List of available words, taken from the Small World of Words

import numpy as np
from sknetwork.data import load_netset
from create_embeddings import create_or_load_embeddings
import pdb

data = load_netset("swow")
adjacency = data.adjacency  # graph (if needed)
words = [str(word) for word in data.names]  # words

# Functions to complete; your code must run fast (less than 100ms on a laptop)

table = create_or_load_embeddings(words, model_name="all-MiniLM-L6-v2", batch_size=128)

def speak(
    n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()
) -> str:
    """
    Give a word to other players.
    The word must belong to the list of available words.
    It cannot be the secret word, nor a word that has already been given.

    Parameters
    ----------
    n_players: int
        Number of players.
    player: int
        Your player id (from 1 to n_players).
    secret_word: string
        Your secret word (empty string if Mr White).
    list_words: list of string
        List of words given since the start of the game (empty if you start).
    list_players: list of int
        List of players having spoken since the start of the game (empty if you start).
    roles: dict
        Known roles.
        Key = player, Value = role ("C" for Civilian, "U" for Undercover, "W" for Mr White).

    Examples
    --------
    > speak(5, 4, "cat", ["milk"], [3])
    > "lion"

    > speak(5, 4, "cat", ["milk", "lion", "house", "cheese", "friend"], [3, 4, 2, 1, 5], {2: "U"})
    > "sleep"
    """
    if len(secret_word):
        return speak_adjacency(n_players, player, secret_word, list_words, list_players, roles)
    else:
        return speak_random(words, n_players*player % len(words))

def speak_random(words, seed):
    return words[seed]

def speak_adjacency(n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()) -> str:
    pdb.set_trace()
    # find words adjacent to secret_word, enough to have a new word


def compute_distance(main_word, other_words):
    d = np.expand_dims(table[main_word], axis=0) - np.concatenate([table[w] for w in other_words], axis=0)
    d = np.linalg.norm(d, axis=1)
    return d



def vote(
    n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()
) -> int:
    """
    Vote for a player to eliminate at the end of a round.
    The returned player index cannot be yours, nor a player that has already been eliminated (role known).

    Parameters
    ----------
    n_players: int
        Number of players.
    player: int
        Your player id (from 1 to n_players).
    secret_word: string
        Your secret word (empty string if Mr White).
    list_words: list of string
        List of words given since the start of the game (empty if you start).
    list_players: list of int
        List of players having spoken since the start of the game (empty if you start).
    roles: dict
        Known roles.
        Key = player, Value = role ("C" for Civilian, "U" for Undercover, "W" for Mr White).

    Example
    -------
    > vote(5, 4, "cat", ["milk", "lion", "house", "cheese", "friend"], [3, 4, 2, 1, 5])
    > 2
    """
    if len(secret_word):
        return vote_nonwhite(n_players, player, secret_word, list_words, list_players, roles)
    else:
        return vote_white(n_players, player, list_words, list_players, roles)

def vote_nonwhite(n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()) -> int:
    distances = compute_distance(secret_word, list_words)
    closest = np.argmin(distances, axis=0).int()
    return list_players[closest]

def vote_white(n_players, player, list_words=[], list_players=[], roles=dict()) -> int:
    votei = 0
    while list_players[votei]==player:
        votei+=1
    return list_players[votei]

def guess(n_players, player, list_words=[], list_players=[], roles=dict()) -> str:
    """
    You are Mr White and you have just been eliminated.
    Guess the secret word of Civilians.

    Parameters
    ----------
    n_players: int
        Number of players.
    player: int
        Your player id (from 1 to n_players).
    list_words: list of string
        List of words given since the start of the game (empty if you start).
    list_players: list of int
        List of players having spoken since the start of the game (empty if you start).
    roles: dict
        Known roles (including yours as Mr White).
        Key = player, Value = role ("C" for Civilian, "U" for Undercover, "W" for Mr White).

    Example
    -------
    > guess(5, 1, ["milk", "lion", "house", "cheese", "friend"], [3, 4, 2, 1, 5])
    > "cat"
    """
    return None
