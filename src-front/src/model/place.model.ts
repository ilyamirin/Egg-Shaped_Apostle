import {Deserializable} from './deserializable.model';


export class Place implements Deserializable {
  id: number;

  seatNumber: number;

  date: Date;

  text: string;

  deserialize(input: any): this {
    Object.assign(this, input);

    return this;
  }

}
