import React from 'react'
import Card from '../card/card.component'

import './card-list.styles.css'


const CardList = (props) => {
  return (
    <div className='card-list'>
      {props.monsters.map((monster, index)=> <Card key={index} monster = {monster} />)}  
    </div>
  );
};

export default CardList;