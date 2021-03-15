import React, {useState} from 'react';
import './Beam.css';
import REDCAP from './prism_datadictionary.json';
import RedcapFilter from './Redcapfilter';
import {
  Link
} from "react-router-dom";


function TableRow(props){
  return (
    <tr className="filter_row" onClick={() => props.added(props.data.name)}>
      <td>{props.data.name}</td>
      <td>{props.data.type}</td>
      <td>{props.data.form_name}</td>
      <td>{props.data.label}</td>
      <td>0</td>
    </tr>
  )
}

function FilterBox(props) {
  const [showBox, setShowBox] = useState(false);
  const [textFilter, setTextFilter] = useState("");
  const [filteredCategories, setCategoryFilter] = useState([]);

  let category_names = [];
  for(let row of props.data){
    if(category_names.indexOf(row.form_name) === -1){
      category_names.push(row.form_name);
    }
  }

  const categories = category_names.map(name =>
    <div key={name}
         style={{ backgroundColor: (filteredCategories.indexOf(name) >= 0 ? 'pink' : 'white') }}
         onClick={() => {
          let newFilter = filteredCategories.slice();
          if(newFilter.indexOf(name) >= 0){
            newFilter.pop(name);
          } else {
            newFilter.push(name);
          }
          setCategoryFilter(newFilter);
         }}
         className="category_box">
      <span className="category_name">{name}</span>
    </div>
  );

  function added(name){
    setShowBox(false);
    setTextFilter("");
    props.added(name);
  }

  const filters = props.data.filter(row =>
    filteredCategories.length === 0 ||
    filteredCategories.indexOf(row.form_name) >= 0
  ).filter(row =>
    textFilter.length === 0 ||
    row.label.toLowerCase().indexOf(textFilter.toLowerCase()) >= 0
  ).map(row =>
    <TableRow data={row} key={row.name} added={added}/>
  );

  return (
    <div className="filter_div">
      <span className="filter_type">{props.must} Have</span>
      <div className="filter_container">
        <div className="filter_spreader">
          <div className="filter_search_box">
            <div className="filter_form">
              <input className="filter_search_input"
                     type="text"
                     value={textFilter}
                     onChange={(e) => {
                       setTextFilter(e.target.value);
                       setShowBox(true);
                     }}
                     placeholder="Search Term..."/>
              <svg className="filter_button" viewBox="0 0 490 490">
                <path fill="none" stroke="#000" strokeWidth="36" d="m280,278a153,153 0 1,0-2,2l170,170m-91-117 110,110-26,26-110-110"/>
              </svg>
            </div>
            <span className="explore_button" onClick={() => setShowBox(!showBox)}>
              <svg height="1em" width="1em" viewBox="0 0 512 512">
                <path d="m478.387 321.984h-28.847l-51.232-62.619c-6.409-7.836-15.892-12.33-26.016-12.33h-106.292v-57.02h94.969c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-60.565c-5.522 0-10 4.478-10 10s4.478 10 10 10h60.565c7.507 0 13.613 6.106 13.613 13.613v66.359c0 7.507-6.106 13.613-13.613 13.613h-209.938c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h60.666c5.522 0 10-4.478 10-10s-4.478-10-10-10h-60.666c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h94.969v57.02h-106.697c-10.124 0-19.606 4.494-26.015 12.329l-51.233 62.62h-28.442c-18.534 0-33.613 15.079-33.613 33.614v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-12.077l40.873-49.957c2.596-3.173 6.436-4.992 10.535-4.992h106.697v54.949h-23.18c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c0-18.534-15.079-33.613-33.613-33.613h-23.179v-54.949h106.292c4.1 0 7.939 1.819 10.536 4.993l40.872 49.956h-11.673c-18.534 0-33.613 15.079-33.613 33.613v66.359c0 18.534 15.079 33.613 33.613 33.613h66.359c18.534 0 33.613-15.079 33.613-33.613v-66.359c.001-18.535-15.078-33.614-33.612-33.614zm-364.801 33.614v66.359c0 7.507-6.106 13.613-13.613 13.613h-66.36c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.507-.001 13.614 6.106 13.614 13.613zm189.207 0v66.359c0 7.507-6.106 13.613-13.613 13.613h-66.36c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.508-.001 13.614 6.106 13.614 13.613zm189.207 66.359c0 7.507-6.106 13.613-13.613 13.613h-66.359c-7.507 0-13.613-6.106-13.613-13.613v-66.359c0-7.507 6.106-13.613 13.613-13.613h66.359c7.507 0 13.613 6.106 13.613 13.613z"/>
                <path d="m246.77 70.25c2.067 5.039 8.028 7.494 13.05 5.41 5.03-2.087 7.501-8.014 5.41-13.051-2.091-5.036-8.012-7.509-13.06-5.42-5.024 2.079-7.488 8.045-5.4 13.061z"/>
              </svg>
            </span>
          </div>
          <div className="filter_results_container" style={{display: (showBox ? 'block' : 'none')}}>
            <div className="category_container">
              {categories}
            </div>
            <div className="filter_list">
              <table className="filter_table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Data Type</th>
                    <th>Form Category</th>
                    <th>Description</th>
                    <th>Count</th>
                  </tr>
                </thead>
                <tbody>
                  {filters}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

function Beam() {
  const [mustFilters, setMustFilters] = useState([]);
  const [cannotFilters, setCannotFilters] = useState([]);

  function add_must_filter(name){
    let newFilters = mustFilters.slice();
    newFilters.push(name);
    setMustFilters(newFilters);
  }

  function add_cannot_filter(name){
    let newFilters = cannotFilters.slice();
    newFilters.push(name);
    setCannotFilters(newFilters);
  }

  function get_data(name){
    for(let row of REDCAP){
      if(row.name === name){
        return row
      }
    }
  }

  const mustFilterBoxes = mustFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row}/>
  );

  const cannotFilterBoxes = cannotFilters.map(row =>
    <RedcapFilter data={get_data(row)} key={row}/>
  );

  return (
    <div>
      <header className="Beam-header">
        <div className="header_section">
          <h2 className="header_title">Current Cohort</h2>
          <input className="cohort_name" placeholder="Unnamed"/>
          <div className="flex_row">
            <button>Save</button>
            <button>New</button>
          </div>
        </div>
        <div className="header_section">
          <h2 className="collection_size header_title">Collection Size</h2>
          <span>1,082 subjects</span>
          <br/>
          <span>{REDCAP.length} data elements</span>
        </div>
        <div className="header_section">
          <h2 className="header_title">Current Cohort</h2>
          <div className="row_flex">
            <div>
              <h4>0 subjects</h4>
              <button className="cohort_size_button">
                <svg version="1.1" viewBox="0 0 65 70" height="2em" with="2em">
                  <g>
                  	<g fill="#555753" opacity="0.3">
                  		<path d="m32.5 4.999c-5.405 0-10.444 1.577-14.699 4.282l-5.75-5.75v16.11h16.11l-6.395-6.395c3.18-1.787 6.834-2.82 10.734-2.82 12.171 0 22.073 9.902 22.073 22.074 0 2.899-0.577 5.664-1.599 8.202l4.738 2.762c1.47-3.363 2.288-7.068 2.288-10.964 0-15.164-12.337-27.501-27.5-27.501z"/>
                  		<path d="m43.227 51.746c-3.179 1.786-6.826 2.827-10.726 2.827-12.171 0-22.073-9.902-22.073-22.073 0-2.739 0.524-5.35 1.439-7.771l-4.731-2.851c-1.375 3.271-2.136 6.858-2.136 10.622 0 15.164 12.336 27.5 27.5 27.5 5.406 0 10.434-1.584 14.691-4.289l5.758 5.759v-16.112h-16.111l6.389 6.388z"/>
                  	</g>
                  </g>
                </svg>
                <span>Count Subjects</span>
              </button>
            </div>
            <Link to="/facet" style={{textDecoration: 'none'}}>
              <button className="tallButton">
                <svg
                  fill="currentColor"
                  viewBox="0 0 16 16"
                  height="3em"
                  width="3em">
                  <path
                    fillRule="evenodd"
                    d="M.5 9.9a.5.5 0 01.5.5v2.5a1 1 0 001 1h12a1 1 0 001-1v-2.5a.5.5 0 011 0v2.5a2 2 0 01-2 2H2a2 2 0 01-2-2v-2.5a.5.5 0 01.5-.5z"
                  />
                  <path
                    fillRule="evenodd"
                    d="M7.646 11.854a.5.5 0 00.708 0l3-3a.5.5 0 00-.708-.708L8.5 10.293V1.5a.5.5 0 00-1 0v8.793L5.354 8.146a.5.5 0 10-.708.708l3 3z"
                  />
                </svg>
                <span>Browse Files</span>
              </button>
            </Link>
          </div>
        </div>
      </header>
      <div className="filters">
        <div className="filter_item_container">
          <FilterBox must="MUST" data={REDCAP} added={add_must_filter}/>
          {mustFilterBoxes}
        </div>
        <div className="filter_item_container">
          <FilterBox must="CANNOT" data={REDCAP} added={add_cannot_filter}/>
          {cannotFilterBoxes}
        </div>
      </div>
    </div>
  );
}

export default Beam;