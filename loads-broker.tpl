#!/bin/bash
source molotov.env && \
echo "Building loads-broker.json" && \
cat > loads-broker.json <<EOF
{
  "name": "Loadtest: Firefox Screenshots Server Testing",
  "plans": [

    {
      "name": "Loadtest",
      "description": "4 boxes",
      "steps": [
        {
          "name": "Screenshots",
          "instance_count": 4,
          "instance_region": "us-east-1",
          "instance_type": "m3.medium",
          "run_max_time": 3600,
          "container_name": "firefoxtesteng/screenshots-loadtests:latest",
          "environment_data": [
            "URL_SERVER=https://screenshots.stage.mozaws.net",
            "TEST_PROCESSES=10",
            "TEST_DURATION=600",
            "TEST_CONNECTIONS=100"
          ],
          "volume_mapping": "/var/log:/var/log/$RUN_ID:rw",
          "docker_series": "screenshots_tests"
        }
      ]
    }
  ]
}
EOF