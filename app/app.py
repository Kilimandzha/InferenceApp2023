import json

import gradio as gr

import requests
import yaml

yandex_token = ""
with open("../secrets.yaml", "r") as stream:
    try:
        secrets = yaml.safe_load(stream)
        yandex_token = secrets["yandex_token"]
    except yaml.YAMLError as exc:
        print(exc)

YANDEX_URL = "https://iam.api.cloud.yandex.net/iam/v1/tokens"
NODE_URL = (
    "https://datasphere.api.cloud.yandex.net/datasphere/v1/nodes/:execute"
)
MODEL = None


def predict(sentence: str):
    print(json.dumps({"sentence":sentence}))
    model_response = requests.post(
        NODE_URL, data=json.dumps("{\"sentence\": \"" + sentence + "\"}"),
    )
    if model_response.ok:
        prob = model_response.json()["answer"]
        return (
            prob["1"],
            prob["0"],
            prob["-1"],
            prob["Communication"],
            prob["Quality"],
            prob["Price"],
            prob["Safety"],
        )
    else:
        return 0


if __name__ == "__main__":
    print("App started")
    response = requests.post(
        YANDEX_URL + f"?yandexPassportOauthToken={yandex_token}"
    )
    if response.ok:
        iamtoken = response.json()["iamToken"]
    else:
        exit(1)

    MODEL = lambda x: x * 10  # load model

    demo = gr.Interface(
        fn=predict,
        title="Try it yourself!",
        inputs=gr.Textbox(lines=3, placeholder="Sentence here..."),
        outputs=[
            gr.Number(0.0, label="1"),
            gr.Number(0.0, label="0"),
            gr.Number(0.0, label="-1"),
            gr.Number(0.0, label="Communication"),
            gr.Number(0.0, label="Quality"),
            gr.Number(0.0, label="Price"),
            gr.Number(0.0, label="Safety"),
        ],
    )

    demo.launch(server_name="0.0.0.0", server_port=8080)
