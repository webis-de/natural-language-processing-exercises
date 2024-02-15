# Submissions of TIRA_USER_FOR_AUTOMATIC_REPLACEMENT

This repository contains baseline submissions (document-processing, query-processing, re-ranking, and retrieval) together with a Github action and a development container configuration as starting point for submissions for the [](). 

We recommend that you work either in Github Codespaces or using [dev containers with Docker](https://code.visualstudio.com/docs/devcontainers/containers). Github Codespaces are an easy option to start in a few minutes (free tier of 130 compute hours per month), whereas dev container with Docker might be interesting if you want to put a bit more focus on technical/deployment details.


## Developing in Github Codespaces

- Open this repository in Github Codespaces (i.e., click on "Code" -> "Codespaces" -> "Create ...").
- Please do not forget to commit often


## Developing in Dev Containers

A dev container (please find a suitable installation instruction [here](https://code.visualstudio.com/docs/devcontainers/containers)) allows you to directly work in the prepared Docker container so that you do not have to install the dependencies (which can sometimes be a bit tricky).

To develop with dev containers, please:

- Install [VS Code](https://code.visualstudio.com/download) and [Docker](https://docs.docker.com/engine/install/) on your machine
- Clone this repository: `git clone ...`
- Open the directory `jupyter-notebook-submissions` with VS Code (it should ask you to open the repository in a dev container)

If you do not want to use VS Code, you can start and develop in a jupyter notebook via (please execute the command within the `jupyter-notebook-submissions` directory):

```
docker run --rm  -it -p 8888:8888 --entrypoint jupyter -w /workspace -v ${PWD}:/workspace webis/ir-lab-wise-2023:0.0.1 notebook --allow-root --ip 0.0.0.0
```

## Submitting Your Software

Run the github action to submit your software.

