import React from 'react';

function object_to_array(row){
  return Object.keys(row).map((key) => row[key]);
}

function DataTable(props) {
  if (!props.data.hasOwnProperty("columns")){
    return <></>;
  }
  let columns = props.data.columns;
  const headers = columns.map((name, i) => <th key={'h' + i}>{name}</th>)

  const rows = props.data.data.map((row, ri) =>
    <tr key={'row' + ri}>
      {row.map((value, i) => <td key={'r' + ri + 'i' + i}>{value}</td>)}
    </tr>);
  return (
    <table>
      <thead>
        <tr>{headers}</tr>
      </thead>
      <tbody>
        {rows}
      </tbody>
    </table>
  );
}

export default DataTable;
