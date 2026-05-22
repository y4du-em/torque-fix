import type { VehicleType } from "@torquefix/types";

export interface VehicleMake {
  id: string;
  name: string;
  types: VehicleType[];
  models: VehicleModel[];
}

export interface VehicleModel {
  id: string;
  name: string;
  years: number[];
  engineCC: number[];
  fuelTypes: string[];
  type: VehicleType;
}

export interface Symptom {
  id: string;
  label: string;
}

export const vehicleData: VehicleMake[] = [
  {
    id: "honda",
    name: "Honda",
    types: ["bike", "scooter"],
    models: [
      {
        id: "cb-shine",
        name: "CB Shine",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [125],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "hornet-2-0",
        name: "Hornet 2.0",
        years: [2020, 2021, 2022, 2023, 2024],
        engineCC: [184],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "cbr-150r",
        name: "CBR 150R",
        years: [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [150],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "activa-6g",
        name: "Activa 6G",
        years: [2020, 2021, 2022, 2023, 2024],
        engineCC: [110],
        fuelTypes: ["petrol"],
        type: "scooter",
      },
    ],
  },
  {
    id: "yamaha",
    name: "Yamaha",
    types: ["bike", "scooter"],
    models: [
      {
        id: "mt-15-v2",
        name: "MT-15 V2",
        years: [2022, 2023, 2024],
        engineCC: [155],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "fz-s-v3",
        name: "FZ-S V3",
        years: [2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [149],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "r15-v4",
        name: "R15 V4",
        years: [2021, 2022, 2023, 2024],
        engineCC: [155],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "fascino-125",
        name: "Fascino 125",
        years: [2020, 2021, 2022, 2023, 2024],
        engineCC: [125],
        fuelTypes: ["petrol"],
        type: "scooter",
      },
    ],
  },
  {
    id: "royal-enfield",
    name: "Royal Enfield",
    types: ["bike"],
    models: [
      {
        id: "bullet-350",
        name: "Bullet 350",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [346],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "classic-350",
        name: "Classic 350",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [346],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "meteor-350",
        name: "Meteor 350",
        years: [2021, 2022, 2023, 2024],
        engineCC: [349],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "himalayan",
        name: "Himalayan",
        years: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [411],
        fuelTypes: ["petrol"],
        type: "bike",
      },
    ],
  },
  {
    id: "ktm",
    name: "KTM",
    types: ["bike"],
    models: [
      {
        id: "duke-200",
        name: "Duke 200",
        years: [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [199],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "duke-390",
        name: "Duke 390",
        years: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [373],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "rc-390",
        name: "RC 390",
        years: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [373],
        fuelTypes: ["petrol"],
        type: "bike",
      },
    ],
  },
  {
    id: "bajaj",
    name: "Bajaj",
    types: ["bike"],
    models: [
      {
        id: "pulsar-ns200",
        name: "Pulsar NS200",
        years: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [199],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "pulsar-150",
        name: "Pulsar 150",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [149],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "dominar-400",
        name: "Dominar 400",
        years: [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [373],
        fuelTypes: ["petrol"],
        type: "bike",
      },
    ],
  },
  {
    id: "tvs",
    name: "TVS",
    types: ["bike", "scooter"],
    models: [
      {
        id: "apache-rtr-200",
        name: "Apache RTR 200",
        years: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [197],
        fuelTypes: ["petrol"],
        type: "bike",
      },
      {
        id: "jupiter-125",
        name: "Jupiter 125",
        years: [2021, 2022, 2023, 2024],
        engineCC: [124],
        fuelTypes: ["petrol"],
        type: "scooter",
      },
      {
        id: "ntorq-125",
        name: "NTORQ 125",
        years: [2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [124],
        fuelTypes: ["petrol"],
        type: "scooter",
      },
    ],
  },
  {
    id: "maruti-suzuki",
    name: "Maruti Suzuki",
    types: ["car"],
    models: [
      {
        id: "swift",
        name: "Swift",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197, 1248],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "baleno",
        name: "Baleno",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197],
        fuelTypes: ["petrol"],
        type: "car",
      },
      {
        id: "dzire",
        name: "Dzire",
        years: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197, 1248],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "vitara-brezza",
        name: "Vitara Brezza",
        years: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1462],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
    ],
  },
  {
    id: "hyundai",
    name: "Hyundai",
    types: ["car"],
    models: [
      {
        id: "i20",
        name: "i20",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197, 1497],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "creta",
        name: "Creta",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1497, 1582],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "venue",
        name: "Venue",
        years: [2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197, 1493],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "verna",
        name: "Verna",
        years: [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1497, 1582],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
    ],
  },
  {
    id: "tata",
    name: "Tata",
    types: ["car"],
    models: [
      {
        id: "nexon",
        name: "Nexon",
        years: [2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1199, 1497],
        fuelTypes: ["petrol", "diesel", "electric"],
        type: "car",
      },
      {
        id: "altroz",
        name: "Altroz",
        years: [2020, 2021, 2022, 2023, 2024],
        engineCC: [1199, 1497],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "punch",
        name: "Punch",
        years: [2021, 2022, 2023, 2024],
        engineCC: [1199],
        fuelTypes: ["petrol", "electric"],
        type: "car",
      },
      {
        id: "harrier",
        name: "Harrier",
        years: [2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1956],
        fuelTypes: ["diesel"],
        type: "car",
      },
    ],
  },
  {
    id: "toyota",
    name: "Toyota",
    types: ["car"],
    models: [
      {
        id: "innova-crysta",
        name: "Innova Crysta",
        years: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [2393, 2755],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "fortuner",
        name: "Fortuner",
        years: [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [2694, 2755],
        fuelTypes: ["petrol", "diesel"],
        type: "car",
      },
      {
        id: "glanza",
        name: "Glanza",
        years: [2019, 2020, 2021, 2022, 2023, 2024],
        engineCC: [1197],
        fuelTypes: ["petrol"],
        type: "car",
      },
    ],
  },
];

export const symptomsByCategory: Record<string, Symptom[]> = {
  engine: [
    { id: "eng-001", label: "Engine won't start or hard to start" },
    { id: "eng-002", label: "Rough idling or engine vibration at idle" },
    { id: "eng-003", label: "Loss of power or sluggish acceleration" },
    { id: "eng-004", label: "Engine misfiring or backfiring" },
    { id: "eng-005", label: "Knocking or pinging noise from engine" },
    { id: "eng-006", label: "Excessive oil consumption" },
    { id: "eng-007", label: "Engine stalling while driving" },
    { id: "eng-008", label: "Check engine light illuminated" },
  ],
  brakes: [
    { id: "brk-001", label: "Squealing or grinding noise when braking" },
    { id: "brk-002", label: "Brake pedal feels spongy or soft" },
    { id: "brk-003", label: "Vehicle pulls to one side when braking" },
    { id: "brk-004", label: "Brake pedal sinks to the floor" },
    { id: "brk-005", label: "Vibration or pulsation in brake pedal" },
    { id: "brk-006", label: "Brake warning light on dashboard" },
    { id: "brk-007", label: "Burning smell after braking" },
    { id: "brk-008", label: "Longer stopping distances than usual" },
  ],
  electrical: [
    { id: "elc-001", label: "Battery draining quickly or dead battery" },
    { id: "elc-002", label: "Lights flickering or not working" },
    { id: "elc-003", label: "Starter motor clicking but engine not cranking" },
    { id: "elc-004", label: "Alternator warning light on" },
    { id: "elc-005", label: "Horn not working" },
    { id: "elc-006", label: "Dashboard warning lights illuminated" },
    { id: "elc-007", label: "Electrical accessories not functioning" },
    { id: "elc-008", label: "Blown fuses frequently" },
  ],
  transmission: [
    { id: "trn-001", label: "Difficulty shifting gears or gear slipping" },
    { id: "trn-002", label: "Clutch slipping or not engaging properly" },
    { id: "trn-003", label: "Grinding noise when changing gears" },
    { id: "trn-004", label: "Vehicle jerks or hesitates during acceleration" },
    { id: "trn-005", label: "Transmission fluid leaking" },
    { id: "trn-006", label: "Gear lever feels stiff or hard to operate" },
    { id: "trn-007", label: "Engine revs high but vehicle moves slowly" },
    { id: "trn-008", label: "Clunking noise when shifting into gear" },
  ],
  suspension: [
    { id: "sus-001", label: "Vehicle bouncing excessively on bumps" },
    { id: "sus-002", label: "Steering feels loose or imprecise" },
    { id: "sus-003", label: "Uneven tyre wear" },
    { id: "sus-004", label: "Clunking or rattling noise over bumps" },
    { id: "sus-005", label: "Vehicle pulling to one side while driving" },
    { id: "sus-006", label: "Front end dipping excessively when braking" },
    { id: "sus-007", label: "Squeaking noise from suspension components" },
    { id: "sus-008", label: "Steering wheel vibration at certain speeds" },
  ],
  fuel: [
    { id: "ful-001", label: "Strong fuel smell from engine bay" },
    { id: "ful-002", label: "Poor fuel economy / mileage drop" },
    { id: "ful-003", label: "Engine spluttering on acceleration" },
    { id: "ful-004", label: "Fuel leaking from vehicle" },
    { id: "ful-005", label: "Engine hesitation when pressing throttle" },
    { id: "ful-006", label: "Black smoke from exhaust" },
    { id: "ful-007", label: "Fuel gauge not reading correctly" },
    { id: "ful-008", label: "Difficulty starting after refuelling" },
  ],
  cooling: [
    { id: "col-001", label: "Engine overheating or temperature gauge in red" },
    { id: "col-002", label: "Coolant leaking from engine or hoses" },
    { id: "col-003", label: "Steam or smoke from engine bay" },
    { id: "col-004", label: "Coolant warning light on" },
    { id: "col-005", label: "Radiator fan not working" },
    { id: "col-006", label: "Coolant level dropping without visible leak" },
    { id: "col-007", label: "Sweet smell from engine area" },
    { id: "col-008", label: "Heater not producing warm air" },
  ],
  exhaust: [
    { id: "exh-001", label: "Loud exhaust noise or blowing sound" },
    { id: "exh-002", label: "White smoke from exhaust" },
    { id: "exh-003", label: "Blue smoke from exhaust" },
    { id: "exh-004", label: "Black smoke from exhaust" },
    { id: "exh-005", label: "Strong exhaust fumes inside cabin" },
    { id: "exh-006", label: "Rattling noise from exhaust system" },
    { id: "exh-007", label: "Exhaust pipe vibrating excessively" },
    { id: "exh-008", label: "Exhaust emissions test failure" },
  ],
};

export function getMakesByType(type: VehicleType): VehicleMake[] {
  return vehicleData.filter((make) => make.types.includes(type));
}

export function getModelsByMake(makeId: string): VehicleModel[] {
  const make = vehicleData.find((m) => m.id === makeId);
  return make?.models ?? [];
}

export function getYearsByModel(makeId: string, modelId: string): number[] {
  const make = vehicleData.find((m) => m.id === makeId);
  const model = make?.models.find((m) => m.id === modelId);
  return model?.years ?? [];
}

export function getMakeById(makeId: string): VehicleMake | undefined {
  return vehicleData.find((m) => m.id === makeId);
}

export function getModelById(
  makeId: string,
  modelId: string,
): VehicleModel | undefined {
  const make = vehicleData.find((m) => m.id === makeId);
  return make?.models.find((m) => m.id === modelId);
}
