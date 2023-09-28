This is a work in process project focused on digitizing handwritten sheet music for historical record keeping. This software will also be able to work for digitizing hand written sheet music for modern songwriters. The project is broken down into three parts:

Staff Line Detection
	Detect staff lines using a YoloV8 Neural Network in one 	measure sections allowing for detecting curvy staff lines.

Note Detection
	Notes are detected within each measure and their location 	is stored relative to their measure.

Reconstruction
	The note pitch is then determined and the measures are 	combined to form the final piece.