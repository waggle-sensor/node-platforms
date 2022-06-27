# Virtual Node Platform

Contains the specific instructions and `ansible` scripts for the Virtual Node Platform.

## Docker
There are two options to run the Ansible playbooks in a Docker container; with or without [beekeeper](https://github.com/waggle-sensor/beekeeper).
### Beekeeper
Building the node with Beekeeper ([see the usage](https://github.com/waggle-sensor/beekeeper/blob/main/docker-compose.yml#L56)) provides a simple way to test for integration and functionality of Beekepers API and the SSH Tunnel.

See the [README for Beekeeper](https://github.com/waggle-sensor/beekeeper#beekeeper-server)

### Without Beekeeper
In the mode of running without Beekeeper, a user can test that the Ansible playbooks can be built in a Docker container.

Build:
```
docker build -t waggle/vm-minimal .
```

To run the vm-minimal container, we need to override the CMD for the container since we do not have any beekeeper SSH keys present for this mode.
```
docker run -d --name vm-minimal --entrypoint '/bin/sh' waggle/vm-minimal -c '/bin/sleep infinity'
```

Attached to running container if needed:
```
docker exec -it vm-minimal bash
```
