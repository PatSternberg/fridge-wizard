import React from 'react';

export default function ItemList({ returnedFridgeData, removeItem }) {
  if (
      typeof returnedFridgeData !== 'object' ||
      !returnedFridgeData.fridge_data ||
      typeof returnedFridgeData.fridge_data !== 'object'
  ) {
    console.error("Returned data is not in the expected format:", returnedFridgeData);
    return null;
  }

  const { storedItems } = returnedFridgeData.fridge_data;

  return (
      <div>
        {Object.entries(storedItems).map(([category, items]) => (
            <div key={category}>
              <h2>{category}</h2>
              <ul>
                {Object.entries(items).map(([itemName, value]) => {
                  const date = new Date(value);
                  const day = date.getDate();
                  const month = date.getMonth() + 1;
                  const year = date.getFullYear();
                  const formattedDay = day < 10 ? `0${day}` : day;
                  const formattedMonth = month < 10 ? `0${month}` : month;
                  const formattedDate = `${formattedDay}-${formattedMonth}-${year}`;
                  const isBeforeToday = date < new Date();

                  return (
                      <li key={itemName} className="item" style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                  <span style={{ flex: 1, color: isBeforeToday ? 'red' : 'black' }}>
                    {isBeforeToday && <span style={{ marginRight: '0.5em' }}>⚠️ Expired </span>}
                    {itemName}: {formattedDate}
                  </span>
                        <button onClick={() => removeItem(category, itemName)} className="remove-item-button">−</button>
                      </li>
                  );
                })}
              </ul>
            </div>
        ))}
      </div>

  );
}
