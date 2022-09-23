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


### user settings
- what channels to post to
    - i.e., should some things (new pr) be posted to channel
    - while others be sent via dms (ci failure/success)
- what events to post


### logging
- where/how to log?
- sentry?
- slack lol

### make model for prs as well?
- do we want to track prs?

### api app
- app for api endpoints


### ci cd
- python lint
- python test


### favicon!
- add one!


### emoji reactions
- what should we react to?


### TESTS
- webhooks
    - test webhook receivers against different event types
- slack?
    - TODO
- client app
    - 'home' view

ngrok subdomain
- need to attach to some subdomain since it assigns random urls


### auth
- oauth? - https://docs.github.com/en/developers/apps/building-oauth-apps


### django templates
- add base template and clean up a bit

### slack api permissions
- get permissions for dms
- make a new bot?

-------------------------------------------------------
### TODO
----
### 0.0.2


----
### 0.0.1


### home page
- add images!
- add admin link



### threading
- what would be appropriate to thread?


### notify people of comments
- if someone comments -> dm author
- if author requests re review -> dm reviewers


### create models to track ci status
- need to store ci status for each pr to tell when it passes
    - when passes send message
- get commit hash for messages
    - maybe commit message as well
- when ci passes
    - post to slack channel
    - send dm to author
    - send dm to reviewers
    - mark pr as ready for review

### link github usernames to slack usernames
- function for now?
- later on we can add a model for this
    - SlackUser model
        - user fk
        - slack username string


### parse reviewers
- parse reviewers
- make function to dm people
    - send to bot dev channel for now
    - tag author
    - tag reviewers


### [0.0.1] - 2022-09-23
- Initial release!
- Basic Slack integration
- Basic GitHub webhook receiver
- Basic project setup
    - env file support
    - django apps
    - basic models
- Client app, webhook app and core app
- Basic CI

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)
##### Copyright 2022 © Daniel Nazarian.