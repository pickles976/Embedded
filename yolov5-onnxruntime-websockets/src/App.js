import React, { useState, useRef } from "react";
import { Tensor, InferenceSession } from "onnxruntime-web";
import Loader from "./components/loader";
import Streamer from "./components/streaming";
import { detectImage } from "./utils/detect";
import "./style/App.css";

const App = () => {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState("Loading OpenCV.js...");
  const [image, setImage] = useState(null);
  const inputImage = useRef(null);
  const imageRef = useRef(null);
  const canvasRef = useRef(null);

  // configs
  const modelName = "yolov5n.onnx";
  const modelInputShape = [1, 3, 640, 640];
  const topk = 100;
  const iouThreshold = 0.45;
  const confThreshold = 0.2;
  const classThreshold = 0.2;

  // wait until opencv.js initialized
  cv["onRuntimeInitialized"] = async () => {
    // create session
    setLoading("Loading YOLOv5 model...");
    const yolov5 = await InferenceSession.create(`${process.env.PUBLIC_URL}/model/${modelName}`);
    const nms = await InferenceSession.create(`${process.env.PUBLIC_URL}/model/nms-yolov5.onnx`);

    // warmup model
    setLoading("Warming up model...");
    const tensor = new Tensor(
      "float32",
      new Float32Array(modelInputShape.reduce((a, b) => a * b)),
      modelInputShape
    );
    const config = new Tensor("float32", new Float32Array([100, 0.45, 0.2]));
    const { output0 } = await yolov5.run({ images: tensor });
    await nms.run({ detection: output0, config: config });

    setSession({ net: yolov5, nms: nms });
    setLoading(null);
  };

  return (
    <div className="App">
      {loading && <Loader>{loading}</Loader>}
      <div className="header">
        <h1>YOLOv5 Object Detection App</h1>
        <p>
          YOLOv5 object detection application live on browser powered by{" "}
          <code>onnxruntime-web</code>
        </p>
        <p>
          Serving : <code className="code">{modelName}</code>
        </p>
      </div>

      <div className="content">
      <img
          ref={imageRef}
          src="#"
          alt=""
          style={{ display: image ? "block" : "none" }}
          onLoad={() => {
            detectImage(
              imageRef.current,
              canvasRef.current,
              session,
              topk,
              iouThreshold,
              confThreshold,
              classThreshold,
              modelInputShape
            );
          }}
        />
        <canvas
          id="canvas"
          width={modelInputShape[2]}
          height={modelInputShape[3]}
          ref={canvasRef}
        />
      </div>

      <div className="btn-container">
        <Streamer props={{imageRef: imageRef, loadfn: setImage}}/>
      </div>
      
    </div>
  );
};

export default App;
