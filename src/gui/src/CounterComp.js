import { useEffect, useState } from "react";

const CounterComp = (props) =>
{
    const text = props.text;
    const parentId = props.parentId;
    const value_given = props.value ? props.value : 0;
    const handleInputChange = (value_temp) => {
        props.getValue(value_temp, parentId);
    };

    const [value, setValue] = useState(value_given);
    const [disableSubButton, setDisableSubButton] = useState(false);
    const handleAdd = () => {
        var value_temp = value + 1;
        setValue(value_temp);
        handleInputChange(value_temp);
    }

    const handleSub = () => {
        var value_temp = value - 1;
        setValue(value_temp);
        handleInputChange(value_temp);
    }

    useEffect(() => {
        if(value === 0)
            setDisableSubButton(true);
        else
            setDisableSubButton(false);
    },[value])

    return(
        <div>
            <button onClick={handleSub} disabled={disableSubButton}>-</button>
            <span> {text}</span>
            <span> : <b>{value}</b> </span>
            <button onClick={handleAdd}>+</button>
        </div>
    );
}

export default CounterComp;