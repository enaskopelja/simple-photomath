import {React, useState, useEffect} from 'react';

import {
    Segment,
    Divider,
    Loader,
} from "semantic-ui-react";


const Solution = () => {
    const [sol, setSol] = useState("");

    const api = "http://127.0.0.1:5000/api"

    useEffect(() => {
        fetch(api, {method: 'GET'})
            .then(r => r.json()).then(r => {
                console.log(r)
                setSol(r["solution"])
        });
    }, []);


    return(
        <Segment style={{ padding: "5em 1em" }} vertical>
            <Divider horizontal>SOLUTION</Divider>
            {sol === "" ? <Loader active inline='centered' />:
                          <Segment raised textAlign = 'center' style = {{ marginTop: "5em" }}>{sol}</Segment>}
        </Segment>
);
}

export default Solution;

