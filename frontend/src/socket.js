import { io } from "socket.io-client";

let socket = null;
export function initSocket() {
	socket = io({
		withCredentials: true,
		reconnectionAttempts: 5,
	});

	return socket;
}

export function useSocket() {
	return socket;
}
