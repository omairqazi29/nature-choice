
import { useDispatch, useDynamicProperty, createSendActionNameAction, useModule } from "taipy-gui";
import { useMediaStream, useVideo } from "./video";
import { useCanvas } from "./canvas";

interface WebcamProps {
    id?: string;
    onDataReceive: string;
    classname?: string;
    defaultClassname?: string;
    faces?: string[];
    defaultFaces?: string[];
    samplingRate?: number;
}

const Webcam = (props: WebcamProps) => {
    const { id, samplingRate = 50, onDataReceive = "data_received" } = props;

    const faces = useDynamicProperty(props.faces, props.defaultFaces, []);
    const classname = useDynamicProperty(props.classname, props.defaultClassname, "");

    const mediaStream = useMediaStream({ video: true, audio: false });
    const dispatch = useDispatch();
    const module = useModule();

    const sendImage = (blob) => {
        new Response(blob).arrayBuffer().then((data) => {
            const bytes = new Uint8Array(data);
            console.log("Sending " + bytes.length + " bytes.")
            const action = createSendActionNameAction(id, module, onDataReceive, {
                "data": bytes,
            });
            dispatch(action);
        });
    };

    // Draw callback function
    const draw = (ctx, video, frameCount) => {
        // Draw video on canvas
        ctx.drawImage(video, 0, 0);

        // Take snapshot from video every x frames (TODO: add prop for sample rate):
        if (frameCount % samplingRate == 0) {
            ctx.canvas.toBlob(sendImage, 'image/jpeg', 0.95);
        }

        // Draw rectangles on detected faces
        ctx.strokeStyle = "#ff2600";
        ctx.lineWidth = 5;

        for (const face of faces) {
            const [x, y, width, height, name] = face.slice(1, -1).split(", ");
            ctx.strokeRect(x, y, width, height)
            if (name) {
                // Remove quotes around text
                const display = name.replace(/[']/g, '');
                ctx.font = "20px Arial";
                ctx.fillStyle = "red";
                ctx.strokeStyle = "#ff2600";
                ctx.fillText(display, x, +y - 10);
            }
        }

    };

    const videoRef = useVideo(mediaStream);
    const canvasRef = useCanvas(videoRef, draw);

    return (
        <div id={id} className={classname}>
            <video ref={videoRef} autoPlay hidden></video>
            <canvas ref={canvasRef}></canvas>
        </div>
    )
}


export default Webcam;