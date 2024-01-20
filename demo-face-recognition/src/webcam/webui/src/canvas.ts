import { useEffect, useRef } from "react";

const updateCanvasSize = (canvas) => {
    const { width, height } = canvas.getBoundingClientRect()
    if (canvas.width !== width || canvas.height !== height) {
        canvas.width = width
        canvas.height = height
        return true
    }
    return false
};


export const useCanvas = (videoRef, draw, options = {}) => {
    const canvasRef = useRef(null);
    useEffect(() => {
        const canvas = canvasRef.current;
        const context = canvas.getContext(options['context'] || '2d')
        const video = videoRef.current;

        let frameCount = 0;
        let animationFrameId;

        const render = () => {
            frameCount++
            context.save();
            updateCanvasSize(canvas);
            draw(context, video, frameCount)
            context.restore();
            animationFrameId = window.requestAnimationFrame(render)
        }
        render()

        return () => {
            window.cancelAnimationFrame(animationFrameId)
        }
    }, [draw]);

    return canvasRef;
}