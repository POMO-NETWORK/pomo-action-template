# pomo-action-template

## How to use
1.Copy ***./github/workflows/flow.yml*** to new repo dir ***./github/workflow*** . <br>
2.Copy ***Dockerfile*** & ***deployment.yaml*** to new repo . <br>
3.Edit "test" jobs for testing, if the job have NOT been edit, the job will just print a simple line of text and pass.

## Caution
The workflow have five type of branch, please follow the following naming format:
* production -> production
* staging -> staging
* develop -> develop
* feature -> feature/xxxxx
* hotfix -> hotfix/xxxxx

## Current workflow
<img width="801" alt="截圖 2024-03-21 下午6 00 04" src="https://github.com/POMO-NETWORK/pomo-action-template/assets/36696478/eac04dfa-039b-448b-9b66-0afe9c5ae0e5">
