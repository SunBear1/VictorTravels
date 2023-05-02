import React, { useState } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './DateRangePicker.css'; // import your custom styles

const DateRangePicker = () => {
  const [startDate, setStartDate] = useState(null);
  const [endDate, setEndDate] = useState(null);

  const handleStartDateChange = (date) => {
    setStartDate(date);
  };

  const handleEndDateChange = (date) => {
    setEndDate(date);
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
