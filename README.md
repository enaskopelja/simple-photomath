# Simple Photomath
## Requirements
`python>=3.8`
## Installation
`pip install -r requrements.txt`
## Usage
`python api.py` starts Flask api on `localhost:5000` 

`yarn start` in `frontend/` starts a simple React app for file upload and webcam image capture. 

`POST /api/upload` expects a file named `image`, decodes it, recognizes and solves the written expression. 
Returns a textual representation of the result.