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

#### security
- add webhook secret
    - add to github as well


#### user settings
- what channels to post to
    - i.e., should some things (new pr) be posted to channel
    - while others be sent via dms (ci failure/success)
- what events to post


#### logging
- where/how to log?
- sentry?
- slack lol


#### api app
- app for api endpoints


#### cd
- need to have a deployment env first


#### favicon!
- add one!


#### emoji reactions
- what should we react to?


#### TESTS
- webhooks
    - test webhook receivers against different event types
- slack class somehow
- client app
    - 'home' view
- model tests
    - webhook received
    - github webhook received
- ci


#### auth
- oauth? - https://docs.github.com/en/developers/apps/building-oauth-apps


#### django templates
- add base template and clean up a bit


#### slack api permissions
- get permissions for dms
- make a new bot?


-------------------------------------------------------
### TODO
----
### 0.0.2

#### documentation
- how to run
- how to signup/activate


#### ngrok subdomain
- need to attach to some subdomain since it assigns random urls
- gladis.mercury.com


#### threading
- what would be appropriate to thread?


#### switch to mercury github
- switch to mercury github
- figure out how to add other users


----
### 0.0.1


#### home page
- add images!
- add admin link


#### notify people of comments
- if someone comments -> dm author
- if author requests re review -> dm reviewers


#### ci status updates
- get commit hash for messages
    - maybe commit message as well
- when ci passes
    - send dm to author
    - send dm to reviewers
    - mark pr as ready for review
        - github update functionality? may be somewhat difficult
- when ci fails
    - send dm to author
    - mark pr as not ready for review
    

#### create ci and pr models
- model to track pr
    - probably need to thread and emoji
- need to store ci status for each pr to tell when it passes
    - when passes send message


### [0.0.1] - 2022-09-23
- Initial release!
- Basic Slack integration and message sending
- Basic GitHub webhook receiver and parsing
- Basic project setup
    - env file support
    - django apps
    - basic models
- Client app, webhook app and core app
- Basic CI

-------------------------------------------------------

##### [https://danielnazarian.com](https://danielnazarian.com)
##### Copyright 2022 © Daniel Nazarian.