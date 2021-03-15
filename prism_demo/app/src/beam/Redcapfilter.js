import React from 'react';
import './Redcapfilter.css';
import NumberRangeFilter from './NumberRangeFilter';
import RadioFilter from './RadioFilter';

function check_boxes(choices){
  return choices.map((choice) =>
    <label key={choice.value}>
      <input type='checkbox' value={choice.value}/>
      {choice.label}
    </label>
  );
}

function RedcapFilter(props) {
  if(!props.data) return <form></form>
  let input = <label>missing {props.data.type}</label>
  if(props.data.type === 'text'){
    input = <div>
              <p>Filter for values, * is wildcard</p>
              <label>
                Filter <input type='text'/>
              </label>
            </div>
  } else if(props.data.type === 'calc'){
    return <NumberRangeFilter data={props.data} remove={props.remove} fetch={props.fetch}/>
  } else if(['radio', 'checkbox', 'dropdown'].includes(props.data.type)){
    return <RadioFilter data={props.data} remove={props.remove} fetch={props.fetch}/>
  } else if(props.data.type === 'yesno') {
    let yesno = [{'value': 0, 'label': 'Yes'}, {'value': 1, 'label': 'No'}]
    input = check_boxes(yesno);
  }
  return (
    <div class="form_box">
      <button onClick={() => props.remove(props.data.name)}>X</button>
      <h4>{props.data.name}</h4>
      <p>{props.data.label}</p>
      <div class="boxes">
        {input}
      </div>
    </div>
  );
}

export default RedcapFilter;
