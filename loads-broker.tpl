#!/bin/bash
source molotov.env && \
echo "Building loads-broker.json" && \
cat > loads-broker.json <<EOF
{
  "name": "Loadtest: Page Shot Server Testing",
  "plans": [

    {
      "name": "Loadtest",
      "description": "4 boxes",
      "steps": [
        {
          "name": "Page Shot",
          "instance_count": 4,
          "instance_region": "us-east-1",
          "instance_type": "m3.medium",
          "run_max_time": 3600,
          "container_name": "firefoxtesteng/pageshot-loadtests:latest",
          "environment_data": [
            "URL_SERVER=https://pageshot.stage.mozaws.net",
            "TEST_PROCESSES=10",
            "TEST_DURATION=600",
            "TEST_CONNECTIONS=100"
          ],
          "volume_mapping": "/var/log:/var/log/$RUN_ID:rw",
          "docker_series": "pageshot_tests"
        }
      ]
    }
  ]
}
EOF