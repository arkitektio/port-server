# Port-Server

[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/arkitektio/port-server/)
![Maintainer](https://img.shields.io/badge/maintainer-jhnnsrs-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


Port is a central Plugin Store for Arkitekt. It represents a central installation point for Arkitekt Plugins,
that are retrieved from `Repos`. It is designed to install these plugin apps and manage on a connected Container backend (currently
only with Docker). It also provides ways of interacting with the plugin apps and their containers, e.g inspecting logs, or
restarting the container. 

Find mroe about Port in the [documentation](https://arkitekt.live/docs/services/port).


## Developmental Notices

Port is currently being deprecated in favor of [Kabinet](https://github.com/arktektio/kabinet-server) in a **default** Arkitekt Deployment. Kabinet ill replace
it as a central App Store for Arkitekt. This repository will remain the main repository for Port, and Kabinet will live in its own repository.

For most users, Kabinet will be a drop-in replacement for Port, and will provide the same functionality. However, Kabinet will be more modular and
easier to extend. It will also be more secure, as it will be based on the modern Arkitekt Stack of [Django](https://djangoproject.com)  and [Strawberry GraphQL](https://strawberry.rocks/). So please consider migrating to Kabinet.


