import { useEffect, useRef, useState } from "react";

export function useMediaStream(requestedMedia) {
    const [mediaStream, setMediaStream] = useState(null);

    useEffect(() => {
        async function enableStream() {
            try {
                const stream = await navigator.mediaDevices.getUserMedia(requestedMedia);
                setMediaStream(stream);
            } catch (err) {
                console.log("Something bad happend: " + err);
            }
        }

        if (!mediaStream) {
            enableStream();
        }
    }, [mediaStream, requestedMedia]);

    return mediaStream;
}

export const useVideo = (mediaStream) => {
    const videoRef = useRef<HTMLVideoElement>();
    useEffect(() => {
        const video = videoRef.current;
        video.srcObject = mediaStream;
    });
    return videoRef;
}