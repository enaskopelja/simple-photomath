import React from 'react';
import Webcam from 'react-webcam'

import {Button, Embed, Grid} from 'semantic-ui-react'
import 'semantic-ui-css/semantic.min.css'
import {Link} from "react-router-dom";


export default function Camera(){
    const webcamRef = React.createRef();
    const api = "http://127.0.0.1:5000/api/"

    const capture = () => {
        const formData = new FormData();

        formData.append('image', webcamRef.current.getScreenshot());
        console.log(formData.getAll('image'))

        fetch(api + 'webcam', {
            method: 'POST',
            headers: {'enctype': 'multipart/form-data'},
            body: formData
        }).then();
    }

    return (
        <Grid columns={3} relaxed verticalAlign='middle'  style={{paddingTop:'2em'}}>
            <Grid.Column width={5}/>

            <Grid.Column width={6}>
                <Grid.Row>
                    <Embed aspectRatio = {'4:3'}>
                        <Webcam audio={false} ref={webcamRef} screenshotFormat="image/jpeg"/>
                    </Embed>
                    <Link to="/solution">
                        <Button onClick={capture} attached='bottom'>Capture</Button>
                    </Link>
                </Grid.Row>
            </Grid.Column>

            <Grid.Column width={5}/>
        </Grid>
    );
};



