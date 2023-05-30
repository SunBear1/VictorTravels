import {useEffect, useState} from 'react';

function NumberInput({label, defaultValue, val}) {
    const [value, setValue] = useState(defaultValue || 0);

    const handleIncrement = () => {
        setValue(value + 1);
    };

    const handleDecrement = () => {
        if (value === 0) {
            return;
        }
        setValue(value - 1);
    };

    const handleChange = event => {
        const inputValue = parseInt(event.target.value, 10);
        setValue(isNaN(inputValue) ? 0 : inputValue);
    };

    useEffect(
        () => {
            val(value || 0);
        },
        [value]
    );

    return (
        <div className="custom-number-input h-10 w-32">
            <label className="w-full text-slate-300 text-sm font-semibold">
                {label}
            </label>
            <div className="flex flex-row h-10 w-full rounded-lg relative bg-transparent mt-1">
                <button
                    onClick={handleDecrement}
                    className=" bg-slate-600 text-slate-400 hover:text-slate-300 hover:bg-slate-700 h-full w-20 rounded-l cursor-pointer outline-none"
                >
                    <span className="m-auto text-2xl font-thin">−</span>
                </button>
                <input
                    type="number"
                    className="outline-none focus:outline-none text-center w-full bg-slate-600 font-semibold text-md hover:text-black focus:text-black  md:text-basecursor-default flex items-center text-gray-800  outline-none"
                    value={value}
                    onChange={handleChange}
                />
                <button
                    onClick={handleIncrement}
                    className="bg-slate-600 text-slate-400 hover:text-slate-300 hover:bg-slate-700 h-full w-20 rounded-r cursor-pointer"
                >
                    <span className="m-auto text-2xl font-thin">+</span>
                </button>
            </div>
        </div>
    );
}

export default NumberInput;
