import React from 'react'
import './card.styles.css'

const Card = (props) => {
  return (
    <div className='card-container'>
      <img alt="monsters" src={`https://robohash.org/${props.monster.id}?set=set2&size=150x250`}/>
      <h2>{props.monster.name}</h2>
      <p>{props.monster.email}</p>
    </div>
  );
}

export default Card;