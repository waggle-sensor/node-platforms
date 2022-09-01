## Optional Test to run

- Run command `lsblk` to see the drives configured correctly
> Dev Note: insert in the correct output here

- Check the status of k3s by running this command `service k3s status`
    1. Output should look like this:
    ```bash
    ● k3s.service - Lightweight Kubernetes
    Loaded: loaded (/etc/systemd/system/k3s.service; disabled; vendor preset: enabled)
    Active: inactive (dead)
     Docs: https://k3s.io
    ```

- Execute this command to test if the service is working `service waggle-nodeid status`
    ```bash
    Dev Note: insert correct output here
    ```

### Test k3s and Docker's GPU Access

1. Test k3s service override by running the following commands:
    ```bash
    service k3s status
    systemctl cat k3s
    ```

    - Make sure lan and wan are connected before testing k3s service
        ```
        wan0
        u should have your uplink (to network switch) plugged into the nano ethernet port

        lan0
        u should have the ethernet dongle connected to a usb port
        (this is what you connect the camera to)
        ```
    
        - if this is not the case then you will get this error when running `service k3s status`:
        ```bash
        Process: 7538 ExecStartPre=/usr/bin/nmcli conn up lan (code=exited, status=4)
        ```

    - k3s service should start and the service override should work
    >Dev Note: Insert correct Ouput here

2. If `service k3s status` returns active then test k3s and run basic pod by running the following commands:
    ```bash 
    kubectl get pod -A
    kubectl get node
    ```
    - The output should look like this:
        ```bash
        NAME                           STATUS   ROLES                  AGE   VERSION
        000048b02d5bfe58.wd-nanocore   Ready    control-plane,master   19h   v1.20.2+k3s1
        ```
3. Test dnsmasq by running the following commands:
    ```bash
    service dnsmasq status
    systemctl cat dnsmasq.service
    ```
    >Dev Note: insert the correct output here

4. Test docker's GPU access by running this command `docker run -ti --rm --gpus all waggle/gpu-stress-test:latest`

    - To see if the gpu is being used check the gpu frequency (GR3D_FREQ) by running this command `tegrastats` in a seperate terminal

5. If `service k3s status` returns active and `kubectl get node` returns an active node then test k3s' GPU access by running this command `kubectl run gpu-test --image=waggle/gpu-stress-test:latest --attach=true`
    > Note: You may see the error `error: timed out waiting for the condition`. that is okay. it just means it is taking a long time to create the container in `k3s`

    - It takes a while for the pod to create, to watch the pod creation status run this command `watch kubectl get pod`

    - To see if the gpu is being used check the gpu frequency (GR3D_FREQ) by running this command `tegrastats` in a seperate terminal

6. Once the pod stops running (~5 min) delete the pod by running this command `kubectl delete pod gpu-test &`

### Testing the local dev docker registry
1. To test the local dev docker registry run the following commands:
    ```bash
    curl https://10.31.81.1:5000/v2/_catalog
    ```
    - Output:
    ```bash
    {"repositories":[]}
    ```

2. Ensure you can pull from local registry by running the following commands:
    ```bash
    docker pull ubuntu:latest

    docker tag ubuntu:latest 10.31.81.1:5000/joe:latest

    curl https://10.31.81.1:5000/v2/_catalog
    ```
    - Output
    ```bash
    {"repositories":[]}
    ```

3. Ensure you can push to local registry by running this command:
    ```bash
    docker push 10.31.81.1:5000/joe:latest
    ```
    - Output
    ```bash
    13e8c0db60e7: Pushed
    latest: digest: sha256:0f744430d9643a0ec647a4addcac14b1fbb11424be434165c15e2cc7269f70f8 size: 529
    ```
    > Note: while doing the above `push` you should see logs in `docker logs -f local_registry`

4. You should now see a repository by running this command `curl https://10.31.81.1:5000/v2/_catalog`

    - Output
    ```bash
    {"repositories":["joe"]}
    ```
    

### Testing to see if WES is running

After registration, the Beehive should automatically push WES to the node and start running its pods. To see this run the command `kubectl get pod`
```bash
NAME                                        READY   STATUS              RESTARTS   AGE
wes-audio-server-75847fd59-5ql4n            0/1     Pending             0          11m
wes-gps-server-6dd8f84cb9-pkrvf             0/1     Pending             0          11m
node-exporter-mdc5x                         1/1     Running             0          11m
wes-upload-agent-pcjdn                      1/1     Running             0          11m
wes-scoreboard-679ccdddb7-zfxms             1/1     Running             0          11m
wes-metrics-agent-5frxw                     1/1     Running             0          11m
wes-device-labeler-8vqdh                    1/1     Running             0          11m
wes-node-influxdb-0                         1/1     Running             0          11m
wes-camera-provisioner-1657315800-56t8f     0/1     ContainerCreating   0          4m56s
wes-sciencerule-checker-646b4c6c4-h7clz     1/1     Running             0          11m
wes-data-sharing-service-84b7958dd9-l4642   1/1     Running             4          11m
wes-plugin-scheduler-c665b68b5-72r5z        1/1     Running             0          11m
wes-rabbitmq-0                              1/1     Running             1          11m
wes-node-influxdb-loader-6b58f7474-25k8n    1/1     Running             3          11m
```

- You should start seeing metrics being published to the Beehive data store

```bash
$ curl -s 1-H 'Content-Type: application/json' https://data.sagecontinuum.org/api/v1/query -d '{"start": "-125s","filter": {"vsn": "N001"}}'  | grep uptime
{"timestamp":"2022-07-08T21:37:50.542686843Z","name":"sys.uptime","value":12617.5,"meta":{"host":"000048b02d5bfe58.wd-nanocore","node":"000048b02d5bfe58","vsn":"N001"}}
```