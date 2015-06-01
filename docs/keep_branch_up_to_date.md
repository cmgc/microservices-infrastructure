# Keep remote branch up to date
In this section we will describe procedure how to keep remote feature branch up to date with remote master branch and all risks related to these approaches. 

## Use case

_To be able working with latest change to the core functionality (`master`) we need merge all changes to `qa/features-master-integration`_ 

## Simple way. Pull Request

Simple pull request from `master` to `qa/features-master-integration` can be nice solution but got few limitations:

1. In case if `qa/features-master-integration` haven't merged a long time number of commits and changed files can be unmanageable. 
2. History become messy.

## Rebase. Right but require attentions.

Git rebase is smart way to handle such situation but in case of remote branches in GitHub it leads to some constraints and potential issues. 

### Workflow

_[Useful reference](http://stackoverflow.com/questions/6669288/how-to-keep-up-to-date-with-a-parent-branch-of-a-remote-branch)_

 1. Clone remote repository branch `qa/features-master-integration`:
 
        $ git clone git@github.com:CiscoCloud/microservices-infrastructure.git -b qa/features-master-integration 

 2. Rebase local `qa/features-master-integration` branch to the latest version of remote `master`:

        $ git pull --rebase origin master

    * Case 1: You successfully rebased to `master` and you free to continue with next steps
    * Case 2: You have conflicts:
        
        1. Resolve conflicts 
        2. Add fixed files to git staging `git add <name_of_files>`
        3. Continue rebasing `git rebase --continue`

3. Update remote `qa/features-master-integration` branch

        $ git checkout qa/feqtures-master-integration # if your current branch is different
        $ git push origin qa/features-master-integration

### Constraints and issues

Rebase by itself can be very dangerous especially in case of GitHub. Potentially it can broke your local copy of repo and your fork projects. As result your local changes, pull requests changes can be lost. 

Few recommendations:

1. Before rebasing be sure that all pull requests are merged.
2. For every new development activities clone your projects from scratch (or be careful if you know what you are doing).
3. Destroy old and create new fork if there are needed


