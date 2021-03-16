import React from 'react';
import './Redcapfilter.css';
import NumberRangeFilter from './NumberRangeFilter';
import RadioFilter from './RadioFilter';

function RedcapFilter(props) {
  if(!props.data) return <span>Error</span>

  if(props.data.type === 'calc'){
    return <NumberRangeFilter data={props.data} remove={props.remove} fetch={props.fetch}/>
  } else if(['radio', 'checkbox', 'dropdown'].includes(props.data.type)){
    return <RadioFilter data={props.data} remove={props.remove} fetch={props.fetch}/>
  }
  
  return (
    <div class="form_box">
      <button onClick={() => props.remove(props.data.name)}>X</button>
      <span>Missing Type: {props.data.type}</span>
    </div>
  );
}

export default RedcapFilter;
