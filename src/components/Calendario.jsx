import React from 'react';

const Calendario = ({ eventi }) => {
  return (
    <div>
      <h1>Calendario</h1>
      {/* <ul>
        {eventi.map(evento => (
          <li key={evento.id}>{evento.title} - {evento.date}</li>
        ))}
      </ul> */}
    </div>
  );
};

export default Calendario;