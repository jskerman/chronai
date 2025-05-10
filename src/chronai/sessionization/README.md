# Sessionization (`s12n`)

Sessionization is a crucial step when working with natural language (NL) time series data. It helps determine which events (e.g., user queries or actions) should be grouped together into a single `session`. For instance, with Google Search data, we might observe:

| user\_id | search\_datetime     | search\_text            |
| -------- | -------------------- | ----------------------- |
| 1        | 2025-05-08T09:05:30Z | how to start meditating |
| 1        | 2025-05-08T09:08:12Z | how to deal with stress |
| 1        | 2025-05-08T09:11:45Z | benefits of mindfulness |

These queries are clearly related. Ideally, they should be assigned to the same session. When viewed together, we can infer that the user is exploring meditation and mindfulness to cope with stress. Taken in isolation, each event conveys much less context. This is the value of sessionization.

Naturally, events must belong to the same `user_id` to be considered for the same session. We can also introduce the concept of **splitting** and **non-splitting** categories (see below for more details).

Below, we outline two naïve strategies and one more advanced strategy for sessionization.

---

## Windowed Sessionization (`w-s12n`)

In `w-s12n`, two consecutive events belong to the same session if they occurred within a certain time window (`w_s12n_duration`) of each other. For example:

```python
w_s12n_duration = 60  # seconds
```

| user\_id | search\_datetime     | search\_text | session\_id |
| -------- | -------------------- | ------------ | ----------- |
| 1        | 2025-05-08T09:00:00Z | blah         | 1           |
| 1        | 2025-05-08T09:00:30Z | blah         | 1           |
| 1        | 2025-05-08T09:01:45Z | blah         | 2           |

The last event is not in the same session as the previous one because it occurred 75 seconds later—beyond the 60-second threshold.

### Pros of `w-s12n`

* Simple
* Fast
* Easy to interpret

### Cons of `w-s12n`

* May group unrelated events
* The parameter `w_s12n_duration` is difficult to tune

---

## Semantic Sessionization (`s-s12n`)

In `s-s12n`, two consecutive events are grouped into the same session based on the **semantic similarity** of their text. Specifically, the cosine similarity between their embeddings must exceed a threshold (`s_s12n_score`).

```python
s_s12n_score = 0.5
```

| user\_id | search\_datetime     | search\_text  | session\_id |
| -------- | -------------------- | ------------- | ----------- |
| 1        | 2025-05-09T09:00:00Z | tennis        | 1           |
| 1        | 2025-05-09T09:30:00Z | wimbledon     | 1           |
| 1        | 2025-05-09T09:31:45Z | drum and bass | 2           |

Here, `tennis` and `wimbledon` are semantically similar and grouped in the same session. However, `drum and bass` is not similar enough to be included. Time is irrelevant in this method.

### Pros of `s-s12n`

* Groups semantically consistent events
* Semantic cohesion is tunable via `s_s12n_score`

### Cons of `s-s12n`

* Requires computing many embeddings, which can be slow depending on the model
* `s_s12n_score` is difficult to tune
* One rogue event can break a coherent session
  (e.g., `tennis` → `wimbledon` → `drum and bass` → `the french open` gets split into three sessions, when two would be better)

---

## Windowed-Semantic Sessionization (`ws-s12n`)

This hybrid approach combines the time-based and semantic methods. Two events are assigned to the same session **only if** they are both temporally and semantically consistent.
