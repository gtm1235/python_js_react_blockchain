import React, { useState, useEffect } from "react";
import { Link } from 'react-router-dom';
import { FormGroup, FormControl, Button } from 'react-bootstrap';
import { API_BASE_URL } from "../config";

function ConductTransaction() {
    const [amount, setAmount] = useState(0);
    const [recipient, setRecipient] = useState('');
    const [knownAddresses, setKnownAddresses] = useState([]);


    useEffect(() => {
        fetch(`${API_BASE_URL}/known-addresses`)
            .then(response => response.json())
            .then(json => setKnownAddresses(json));
    }, []);

    const updateRecipient = event => {
        setRecipient(event.target.value);
    }

    const updateAmount = event => {
        setAmount(Number(event.target.value));
    }

    const submitTransaction = () => {
        fetch(`${API_BASE_URL}/wallet/transact`,
            {
                method: 'post',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ recipient, amount })
            }
        ).then(response => response.json())
            .then(json => {
                console.log('submitTransaction json', json);
                alert('Success!!');
            });
    }

    return (
        <div className="ConductTransaction">

            <Button variant="light">
                <Link to='/'>Home</Link>
            </Button>
            <hr />
            <h3>Conduct A Transaction</h3>
            <hr />
            <FormGroup>
                <FormControl
                    input="text"
                    placeholder="recipient"
                    value={recipient}
                    onChange={updateRecipient}
                />
            </FormGroup>
            <br />
            <FormGroup>
                <FormControl
                    input="number"
                    placeholder="amount"
                    value={amount}
                    onChange={updateAmount}
                />
            </FormGroup>
            <hr />
            <div>
                <Button
                    variant="danger"
                    onClick={submitTransaction}
                >
                    Submit
                </Button>
            </div>
            <br />
            <h4>Known Addresses</h4>
            <div>
                {
                    knownAddresses.map((knownAddress, i) => (
                        <span key={knownAddresses}>
                            <u>{knownAddress}</u>{i !== knownAddress.length - 1 ? ', ':''}
                        </span>
                    ))
                }
            </div>
        </div>
    )
}

export default ConductTransaction;