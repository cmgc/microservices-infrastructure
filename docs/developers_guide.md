# Git development workflow

## Basic branches and purposes

* `master`: main branch where the source code of HEAD always reflects a production-ready state for CORE services
* `features-master`: main branch where the source code of HEAD always reflects a production-ready state for none CORE services
* `qa\features-master-integration`: source code of HEAD always reflects a state with the latest delivered development changes for the next release. Some would call this the “integration branch”. This is where any automatic nightly builds are built from.

## features-master - release branch

Merges from: _qa/features-master-integration_

#### Workflow:

1. Use PR to merge changes
2. Manual merging by responsible person after code review
3. Every comit should have tag with versoin number 
4. Use CI to validate commit. Use tags to clone new version.
	1. Test should include multi data-center deployment
5. Minimal security check baseon  security check list (TBA)

## qa/features-master-integration - features not in production yet

#### Workflow:

1. Daily rebase from master to get latest changes and [keep branch up to date](https://github.com/CiscoCloud/microservices-infrastructure/blob/qa/features-master-integration/docs/keep_branch_up_to_date.md)
	1. Use automatic CI to start integrity testing for rebase from master, PR from features or personal triggered etc. 
2. Manual merging by PR after code review by approvers

## master (core services)
Main branch.

#### Workflow

1. Use only PRs from features or personal devs
2. Manual merging by PR after code review by approvers
3. Use git tag when milestone has been reached
4. Satrt CI after merging and build new test
	1. Should include multi data-center deployment
5.  Minimal security check baseon  security check list (TBA)

## feature/*

Branched from: _master_ or _qa/features_master_integration_

#### Workflow:	
	
1. Manual testing
2. Open PR to `master` or `qa/features-master-integration`
3. Get approve from maintainer
4. Merge  with --no-ff option - no fast forward (for local dev)
5. Approved `features/*` branches must be deleted after successfull merge

## fix/*

Branched from: _master_ or _features-master_

#### Workflow:	

1. Manually check testing
2. Open PR to `master` and `features-master` (ci testing)
3. Get approve from maintainer
4. `features-master` - merge with hot fix have to be tagged
5. `master` - merge with hot fix have to be tagged
