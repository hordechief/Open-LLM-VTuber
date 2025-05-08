create ssl for dev environment
``` shell
openssl req -x509 -newkey rsa:2048 -nodes \
  -keyout key.pem -out cert.pem -days 365 \
  -subj "/CN=localhost"
```

frontend/assets/main-DsLaT6SU.js
``` javascript
DEFAULT_WS_URL="wss://10.8.123.4:9604/client-ws",DEFAULT_BASE_URL="https://10.8.123.4:9604"
```

run_server.py
``` python
    uvicorn.run(
        app=server.app,
        host=server_config.host,
        port=server_config.port,
        log_level=console_log_level.lower(),
        ssl_keyfile=os.path.join(os.getcwd(),"ssl","key.pem"),
        ssl_certfile=os.path.join(os.getcwd(),"ssl","cert.pem")
    )
```

