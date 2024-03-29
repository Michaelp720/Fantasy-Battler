import React, { useEffect, useState, useContext } from "react";
import TechCard from "../components/TechCard"
import {PlayerContext} from '../context/player'
import { useNavigate } from "react-router-dom";
import { Button, Segment, Header, CardMeta,
    CardHeader,
    CardDescription,
    CardContent,
    Card,
    Icon,
    Image, CardGroup, Grid} from 'semantic-ui-react'



function LrnTechsContainer(){
    const { player, setPlayer } = useContext(PlayerContext)
    const [unlockedTechs, setUnlockedTechs] = useState([])
    const navigate = useNavigate();
    
    useEffect(() => {
        fetch(`/unlockedtechs/${player['id']}`)
            .then(response => response.json())
            .then(data => setUnlockedTechs(data))
    }, [player])

    function handleClick(){
        console.log(unlockedTechs)
    }

    function navVenture(){
        navigate('/ventures')
      }

    return (
        <Segment>
            <Header as = 'h3' textAlign="center" onClick = {handleClick}>Learn Techniques (-2 AP)</Header>
        <CardGroup itemsPerRow={2}>
            
            {unlockedTechs.map((unlockedTech) => (
                <TechCard key = {unlockedTech['id']} techId = {unlockedTech['id']} players_tech = {true} adv = {true}/>
            ))}
            
        </CardGroup>
        <Header as = "h4" textAlign="center" onClick = {navVenture}>Unlock Techniques by Hunting Beasts</Header>
        </Segment>
    )}

export default LrnTechsContainer