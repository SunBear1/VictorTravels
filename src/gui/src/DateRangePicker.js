import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './DateRangePicker.css'; // import your custom styles

const DateRangePicker = (props) => {
  const [startDate, setStartDate] = useState();
  const [endDate, setEndDate] = useState();

  const handleStartDateChange = (date) => {
    const isoDate = date ? date.toISOString().slice(0, 10) : null;
    setStartDate(date);
    props.getValue(isoDate, endDate?.toISOString().slice(0, 10));
  };

  const handleEndDateChange = (date) => {
    const isoDate = date ? date.toISOString().slice(0, 10) : null;
    setEndDate(date);
    props.getValue(startDate?.toISOString().slice(0, 10), isoDate);
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
