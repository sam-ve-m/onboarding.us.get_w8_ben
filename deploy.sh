#!/bin/bash
fission spec init
fission env create --spec --name get-w8-ben-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name get-w8-ben-fn --env get-w8-ben-env --src "./func/*" --entrypoint main.get_w8_ben --executortype newdeploy --maxscale 3
fission route create --spec --name get-w8-ben-rt --method GET --url /onboarding/get_w8_ben --function get-w8-ben-fn