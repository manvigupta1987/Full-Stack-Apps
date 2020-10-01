import React from 'react'
import './search.styles.css'

const Search = (props) => {
  return (
    <input className='search' 
        type='search' 
        placeholder={props.placeholder} 
        onChange={props.handleChange}/>
  );
}

export default Search