import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './DateRangePicker.css'; // import your custom styles

const DateRangePicker = (props) => {
  const [startDate, setStartDate] = useState(props.startDate);
  const [endDate, setEndDate] = useState(props.endDate);

  const handleStartDateChange = (date) => {
    setStartDate(date);
    props.getValue(date, endDate);
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
    props.getValue(startDate, date);
  };

  return (
    <div className="date-range-picker">
      <label className="date-range-picker__label">Start Date:</label>
      <DatePicker
        className="date-range-picker__input"
        selected={startDate}
        onChange={handleStartDateChange}
      />

      <label className="date-range-picker__label">End Date:</label>
      <DatePicker
        className="date-range-picker__input"
        selected={endDate}
        onChange={handleEndDateChange}
      />
    </div>
  );
};

export default DateRangePicker;
