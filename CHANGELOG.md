# CHANGELOG for GLADIS
#### By: [Daniel Nazarian](https://danielnazarian) 🐧👹
##### Contact me at <dnaz@danielnazarian.com>

-------------------------------------------------------

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


-------------------------------------------------------

## [Released]



-------------------------------------------------------

## [Unreleased]

-----

### security
- add webhook secret
    - add to github as well


### api app
- app for api endpoints


### ci cd
- python lint
- python test


### favicon!
- add one!


### TESTS
- webhooks
    - test webhook receivers against different event types
- slack?
    - TODO
- client app
    - 'home' view

### webhook refactoring
- make GithubWebhookReceiver a child of WebhookReceiver


### auth
- oauth? - https://docs.github.com/en/developers/apps/building-oauth-apps


### django templates
- add base template and clean up a bit

-----

## MVP Features
1. post to slack once ci passes for PRs
	1. if ci fails ping the author and mark as a draft again
2. notify people of comments
	1. if someone comments -> ping author
	2. if author requests re=review -> ping reviewers


-------------------------------------------------------
### TODO
----
### 0.0.1


### home page
- add images!

ngrok subdomain
- need to attach to some subdomain since it assigns random urls


### slack integration
- add slack app?
- send messages on slack
- env variables
    - SLACK_CHANNEL_OVERRIDE
    - SLACK_MENTION_OVERRIDE
    - SLACK_API_KEY
    - if DEBUG use overrides


### test webhook integration
- ensure we can receive github webhooks
- setup ngrok
    - https://ngrok.com/docs/getting-started


### [0.0.1] - 2022-09-DD
- Initial release!
- Basic project setup
    - env file support
    - django apps
    - basic models
- Client app, webhook app and core app
- Basic CI

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)
##### Copyright 2022 © Daniel Nazarian.