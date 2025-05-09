# chronai

![Tests][badge-tests]
![Documentation][badge-docs]

[badge-tests]: https://img.shields.io/github/actions/workflow/status/jskerman/chronai/test.yaml?branch=main
[badge-docs]: https://img.shields.io/readthedocs/chronai

[Read the chronai documentation](https://chronai.readthedocs.io/en/latest/index.html)

The name `chronai` is a contraction of `chrono`, relating to time, and `ai`. The motivation for this repo is to formalise some timeseries analysis algrothims for datasets with the following features:

1. `time` - obviosly
2. `text` - some narural language field
3. `category` - some partition of this data i.e. `user_id`, `area_code`, etc.

The motivating example for this tool-kit is Google Search data, for example:

| user_id | search_datetime      | search_text            |
|---------|----------------------|------------------------|
| 1       | 2025-05-08T13:56:35Z | what does chrono mean  |
| 1       | 2025-05-08T13:58:23Z | what does NLP mean     |
| 2       | 2025-05-08T13:58:23Z | how to center a div    |

The motivating technology for this tool kit is LLMs. Anthropics December 2024 paper [Clio: Privacy-Preserving Insights into Real-World AI Use](https://arxiv.org/abs/2412.13678) details a neat methodology for gleaming observations and insights from a large corpus of conversations with Claude. Nothing was particularly novel about this type of analysis, except in lieu of traditional NLP techniques, LLMs were used. No fancy LDA or even less fancy TF-IDF, just calls to see what Claude thought--a lot of them. I've seen this implemented over and over again in the last 12 months, this tool-kit is an attempt to formalise this "new" data science.

## What's injectable?

1. __Pipeline Orchestrator__ [Default: Dagster]: These tools should play nice with pipeline orchestration tools. Dagster, Airflow, Prefect, Celery etc. If our algorithms are to leverage LLMs, we must expect latency and unexpected failures. It seems responsible to expect these jobs to often be run in on such Pipeline Orechestration tools.

2. __LLM Provider__ [Default: lambda.ai]: The LLM in question should be injectable, of course. [Lambda Inference](https://lambda.ai/inference) fits particularly well for these sorts of workloads as these is a large range of cheap models and rate-limits are not an issue.

3. __Embeddings Model__ [Default: HuggingFace]: Of course if you wish to bring your own embeddings model, that's also allowed.

4. __Trad. DS Routines__ [Default: Sklearn]: Now and then we will need to use traditional DS techniques, these will also be injectable, but must follow the `sklearn` standard model interface.


## What can (should) we do now (later)?

- __Sessionization:__ The act of taking a set of semantically consistant and temporally relevant NL texts and grouping them into one `session` (see glossary).

- __[Trending Topics](https://trends.google.com/trending?geo=GB):__ Akin to what google trends does.

- __Temporal Tagging:__ Tagging a certain categorical dimension with topics with some relevance to a temporal window. For example `user_123` tagged with `Looking for holiday destination` for the window `[2025-05-01, '2025-05-10']`.

- __[Clio](https://arxiv.org/abs/2412.13678):__ While the original paper did not concern itself with time, we should.


## TODO

- [x] Set-up docs
- [x] Set-up tests
- [ ] Set-up appropriate mocks for the injectables
- [ ] Build class interfaces
- [ ] Set-up publishing w/ CICD
- [ ] Set-up readme's for above routines.
- [ ] Set-up glossary
- [ ] Set-up branch rules
