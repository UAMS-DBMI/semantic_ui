import React from 'react';

function BarChart(props) {

  let max = 0;
  let rows = [];
  for(var key in props.data){
    let count = props.data[key].length;
    if(count > max) max = count;
  }
  for(var key in props.data){
    let count = props.data[key].length;
    rows.push(<tr key={key}>
      <th scope="row">{key}</th>
      <td style={{'--size': 'calc(' + count + '/' + max + ')'}}>{count}</td>
    </tr>);
  }
  return (
    <table className="charts-css bar show-labels">
      <thead>
        <tr>
          <th scope='col'>Type</th>
          <th scope='col'>Count</th>
        </tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  );
}

export default BarChart;
