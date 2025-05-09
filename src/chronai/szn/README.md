# Sessionization (`szn`)

Often a very important part of dealing with NL timeseries data, which documents deserve to be merged, we call these merged documents `sessions`. For example, with Google Search data we may have:

| user\_id | search\_datetime     | search\_text            |
| -------- | -------------------- | ----------------------- |
| 1        | 2025-05-08T09:05:30Z | how to start meditating |
| 1        | 2025-05-08T09:08:12Z | how to deal with stress |
| 1        | 2025-05-08T09:11:45Z | benefits of mindfulness |

Notice these searches are related, ideally we should assign them all to the same `session`. When read together, it's clear this user is trying to user meditation / mindfulness to deal with stress. When each row is taken independantly, this is harder to construct. Herein lies the benifit of sessionization.

It goes without saying that for two events to be in the same session they must also belong to the same `user_id`. Here we can introduce a notion of splitting and non-splitting categories (See later).

Here we outline two niave strategies and one more advanced strategy.

## Windowed Sessionization (`w-szn`)

In `w-szn`, two consecutive events belong to the same session if they occured within some threshold duration (`w_szn_duration`) of eachother. For example:

`w_szn_duration = 60`

| user\_id | search\_datetime     | search\_text            | session_id |
| -------- | -------------------- | ----------------------- | ---------- |
| 1        | 2025-05-08T09:00:00Z | blah                    | 1          |
| 1        | 2025-05-08T09:30:00Z | blah                    | 1          |
| 1        | 2025-05-08T10:31:45Z | blah                    | 2          |

Notice the last event is not in session with id `1` as it occured `61` seconds after the previous event.

### Pros of `w-szn`
* Simple,
* Fast, and
* Interpretable.

### Cons of `w-szn`
* Large potential to group unrelated items
* The parameter `w_szn_duration` is hard to tune

## Semantic Sessionization (`s-szn`)

In `s-szn` we consider two consecutive events to be in the same session if the distance between their text embedding vectors is greater than some semantic score threshold (`s_szn_score`). For example:

`s_szn_score = 0.5`

| user\_id | search\_datetime     | search\_text            | session_id |
| -------- | -------------------- | ----------------------- | ---------- |
| 1        | 2025-05-08T09:00:00Z | tennis                  | 1          |
| 1        | 2025-05-09T09:30:00Z | wimbledon               | 1          |
| 1        | 2025-05-09T09:31:45Z | drum and bass           | 2          |

Notice the last event is not in session with id `1` as `drum and bass` is likley is not semantically simmilar enough to `wimbledon`. `tennis` and `wimbledon` are in the same session because they likley are semantically similar. Notice that the duration is unimportant here.

### Pros of `s-szn`
* Grouped items are semantically consistant
* Semantic cohesion across the group can be controlled with `s_szn_score`

### Cons of `s-szn`
* Requires the computing potentially many embeddings, depending on the model this can be very slow.
* The parameter `s_szn_score` is hard to tune
* One _rogue_ event can break up sessions (e.g. `tennis` -> `wimbledon` -> `drum and bass` -> `the french open` is broken into three sessions when really we should have two sessions, one Tennis related and one Drum and Bass related).

## Windowed-Semantic Sessionization (`ws-szn`)

We can compose the previous two sessionization strategies into one, where for two consecutive events to be in the same sessions they must both be temporially and semantically consistant.
