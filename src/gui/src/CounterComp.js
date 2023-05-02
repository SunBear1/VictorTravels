import { useEffect, useState } from "react";

const CounterComp = (props) =>
{
    const text = props.text;
    const parentId = props.parentId;
    const handleInputChange = (event) => {
        props.getValue(value, parentId);
    };

    const [value, setValue] = useState(0);
    const [disableSubButton, setDisableSubButton] = useState(false);
    const handleAdd = () => {
        var value_temp = value + 1;
        setValue(value_temp);
        handleInputChange();
    }

    const handleSub = () => {
        var value_temp = value - 1;
        setValue(value_temp);
        handleInputChange();
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