#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Uncover game

# Compared to the standard game:
# 1. The list of words is constrained.
# 2. The order of players is random at each round.
# 3. The votes are secret.

# List of available words, taken from the Small World of Words

import pdb

import numpy as np
from sknetwork.data import load_netset

from create_embeddings import create_or_load_embeddings

data = load_netset("swow")
adjacency = data.adjacency  # graph (if needed)
words = [str(word) for word in data.names]  # words
word_to_index = {word: i for i, word in enumerate(words)}

# Functions to complete; your code must run fast (less than 100ms on a laptop)

table = create_or_load_embeddings(words, model_name="all-MiniLM-L6-v2", batch_size=128)


def get_turn(roles):
    return len(roles)


def convert_word_list_to_embeddings(word_list):
    word_indices = np.array([word_to_index[word] for word in word_list])
    return table[word_indices]


def cosine_distance(embeddings1, embeddings2):
    return -np.dot(embeddings1, embeddings2.T)


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
    return speak_early(n_players, player, secret_word, list_words, list_players, roles)


def speak_random(words, seed):
    return words[seed]


def speak_early(
    n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()
) -> str:
    # randomly pick a word close to own word which has not been said before
    main_word = secret_word if len(secret_word) else list_words[-1]
    d = compute_distance(table[word_to_index[main_word]], table)
    forbidden_words = list_words
    if len(secret_word):
        forbidden_words.append(secret_word)
    indices = [word_to_index[x] for x in forbidden_words]
    d[indices] = float("inf")
    closest = np.argmin(d, axis=0)
    return words[closest]


def create_select_table(word_list):
    return np.stack([table[ii] for ii, _ in enumerate(word_list)], axis=0)


def compute_distance(main_word, other_words):
    d = -np.dot(other_words, main_word)
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
        return vote_nonwhite(
            n_players, player, secret_word, list_words, list_players, roles
        )
    else:
        return vote_white(n_players, player, list_words, list_players, roles)


def vote_nonwhite(
    n_players, player, secret_word="", list_words=[], list_players=[], roles=dict()
) -> int:
    turn = get_turn(roles)
    current_words = list_words[: n_players - turn]
    current_players = list_players[: n_players - turn]

    if secret_word in current_words:
        player_who_said_secret_word = current_players[current_words.index(secret_word)]
        return player_who_said_secret_word

    current_words_embeddings = convert_word_list_to_embeddings(current_words)
    secret_word_embedding = convert_word_list_to_embeddings([secret_word])
    distances = cosine_distance(secret_word_embedding, current_words_embeddings)

    farthest_player = np.argmax(distances, axis=0).int()
    return current_players[farthest_player]


def vote_white(n_players, player, list_words=[], list_players=[], roles=dict()) -> int:
    # Clustering, into voter random dans le cluster des undercover
    remaining_players = [
        i for i in range(1, n_players + 1) if i != player and i not in roles
    ]
    random_player = np.random.choice(remaining_players)
    return random_player


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
