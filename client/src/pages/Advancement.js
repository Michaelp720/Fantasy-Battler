import React, { useEffect, useState, useContext } from "react";
import CharacterContainer from "../containers/CharacterContainer"
import VenturesContainer from "../containers/VenturesContainer"
import AdvStatsContainer from "../containers/AdvStatsContainer"
import LrnTechsContainer from "../containers/LrnTechsContainer"
import {PlayerContext} from '../context/player'
import {CombatContext} from '../context/combat'
import { Button, Segment, Header, CardMeta,
    CardHeader,
    CardDescription,
    CardContent,
    Card,
    Icon,
    Image, CardGroup, Grid} from 'semantic-ui-react'
    import { useNavigate } from "react-router-dom";
    import AdvImage from "../images/AdvancementBG.jpg"


function Advancement(){
    const { player, setPlayer } = useContext(PlayerContext)
    const navigate = useNavigate();


    function navHome(){
        navigate("/")
    }

    function navVenture(){
        navigate("/ventures")
    }

        return (
        <Segment style={{
            backgroundImage: `url(${AdvImage})`,
            backgroundSize: 'cover', // Adjust as needed
            backgroundPosition: 'center', // Adjust as needed
            width: "auto",
            height: "875px"
          }}>
        <Grid columns={2} centered>
            <Grid.Row>
                <Grid.Column width = {5}>
                    <Button onClick = {navHome}>Home</Button>
                    <Button onClick = {navVenture}>Continue the Hunt...</Button>
                </Grid.Column>
                <Grid.Column>
                </Grid.Column>
            </Grid.Row>
            <Grid.Row>
                <Grid.Column width = {5}>
                    <CharacterContainer character={player} advancement = {true} />
                </Grid.Column>
        
                <Grid.Column>
                    <AdvStatsContainer/>
                    <LrnTechsContainer/>
                </Grid.Column>
            </Grid.Row>
        </Grid>
        </Segment>
    )}

export default Advancement