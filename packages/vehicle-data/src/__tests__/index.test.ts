import { describe, expect, it } from "vitest";
import {
  getMakeById,
  getMakesByType,
  getModelById,
  getModelsByMake,
  getYearsByModel,
  symptomsByCategory,
  vehicleData,
} from "../index";

describe("getMakesByType", () => {
  it("returns only makes that include the requested type", () => {
    // Act
    const bikeMakes = getMakesByType("bike");

    // Assert
    expect(bikeMakes.length).toBeGreaterThan(0);
    bikeMakes.forEach((make) => {
      expect(make.types).toContain("bike");
    });
  });

  it("returns car makes for type car", () => {
    // Act
    const carMakes = getMakesByType("car");

    // Assert
    const names = carMakes.map((m) => m.name);
    expect(names).toContain("Maruti Suzuki");
    expect(names).toContain("Hyundai");
    expect(names).toContain("Tata");
    expect(names).toContain("Toyota");
  });

  it("excludes car makes when filtering for bikes", () => {
    // Act
    const bikeMakes = getMakesByType("bike");

    // Assert
    const names = bikeMakes.map((m) => m.name);
    expect(names).not.toContain("Maruti Suzuki");
    expect(names).not.toContain("Toyota");
  });

  it("returns empty array for type with no matching makes", () => {
    // Act
    const truckMakes = getMakesByType("truck");

    // Assert
    expect(truckMakes).toEqual([]);
  });

  it("returns scooter makes correctly", () => {
    // Act
    const scooterMakes = getMakesByType("scooter");

    // Assert
    expect(scooterMakes.length).toBeGreaterThan(0);
    scooterMakes.forEach((make) => {
      expect(make.types).toContain("scooter");
    });
  });
});

describe("getModelsByMake", () => {
  it("returns all models for a known make", () => {
    // Act
    const models = getModelsByMake("honda");

    // Assert
    expect(models.length).toBeGreaterThan(0);
    const names = models.map((m) => m.name);
    expect(names).toContain("CB Shine");
    expect(names).toContain("Activa 6G");
  });

  it("returns empty array for unknown make id", () => {
    // Act
    const models = getModelsByMake("unknown-make");

    // Assert
    expect(models).toEqual([]);
  });

  it("returns correct models for royal-enfield", () => {
    // Act
    const models = getModelsByMake("royal-enfield");

    // Assert
    const names = models.map((m) => m.name);
    expect(names).toContain("Classic 350");
    expect(names).toContain("Himalayan");
  });
});

describe("getYearsByModel", () => {
  it("returns years for a known make and model", () => {
    // Act
    const years = getYearsByModel("honda", "cb-shine");

    // Assert
    expect(years.length).toBeGreaterThan(0);
    expect(years).toContain(2022);
    expect(years).toContain(2015);
  });

  it("returns empty array for unknown make", () => {
    // Act
    const years = getYearsByModel("unknown", "cb-shine");

    // Assert
    expect(years).toEqual([]);
  });

  it("returns empty array for unknown model", () => {
    // Act
    const years = getYearsByModel("honda", "unknown-model");

    // Assert
    expect(years).toEqual([]);
  });

  it("returns years within expected range", () => {
    // Act
    const years = getYearsByModel("maruti-suzuki", "swift");

    // Assert
    years.forEach((year) => {
      expect(year).toBeGreaterThanOrEqual(2015);
      expect(year).toBeLessThanOrEqual(2024);
    });
  });
});

describe("getMakeById", () => {
  it("returns the make for a known id", () => {
    // Act
    const make = getMakeById("yamaha");

    // Assert
    expect(make).toBeDefined();
    expect(make?.name).toBe("Yamaha");
  });

  it("returns undefined for unknown id", () => {
    // Act
    const make = getMakeById("nonexistent");

    // Assert
    expect(make).toBeUndefined();
  });

  it("returned make has models array", () => {
    // Act
    const make = getMakeById("ktm");

    // Assert
    expect(make?.models).toBeDefined();
    expect(make?.models.length).toBeGreaterThan(0);
  });
});

describe("getModelById", () => {
  it("returns the model for a known make and model id", () => {
    // Act
    const model = getModelById("bajaj", "pulsar-ns200");

    // Assert
    expect(model).toBeDefined();
    expect(model?.name).toBe("Pulsar NS200");
  });

  it("returns undefined for unknown model id", () => {
    // Act
    const model = getModelById("honda", "nonexistent-model");

    // Assert
    expect(model).toBeUndefined();
  });

  it("returns undefined when make id is unknown", () => {
    // Act
    const model = getModelById("nonexistent-make", "cb-shine");

    // Assert
    expect(model).toBeUndefined();
  });

  it("returned model includes fuel types and engine options", () => {
    // Act
    const model = getModelById("tata", "nexon");

    // Assert
    expect(model?.fuelTypes).toContain("petrol");
    expect(model?.fuelTypes).toContain("diesel");
    expect(model?.fuelTypes).toContain("electric");
    expect(model?.engineCC.length).toBeGreaterThan(0);
  });
});

describe("symptomsByCategory", () => {
  const EXPECTED_CATEGORIES = [
    "engine", "brakes", "electrical", "transmission",
    "suspension", "fuel", "cooling", "exhaust",
  ];

  it.each(EXPECTED_CATEGORIES)("has at least 5 symptoms in %s category", (category) => {
    // Act
    const symptoms = symptomsByCategory[category];

    // Assert
    expect(symptoms).toBeDefined();
    expect(symptoms!.length).toBeGreaterThanOrEqual(5);
  });

  it("each symptom has an id and label", () => {
    // Act
    const symptoms = symptomsByCategory["engine"]!;

    // Assert
    symptoms.forEach((symptom) => {
      expect(symptom.id).toBeTruthy();
      expect(symptom.label).toBeTruthy();
    });
  });

  it("symptom ids are unique within a category", () => {
    // Act
    const symptoms = symptomsByCategory["brakes"]!;
    const ids = symptoms.map((s) => s.id);

    // Assert
    expect(new Set(ids).size).toBe(ids.length);
  });
});

describe("vehicleData integrity", () => {
  it("all makes have at least one model", () => {
    vehicleData.forEach((make) => {
      expect(make.models.length).toBeGreaterThan(0);
    });
  });

  it("all models have at least one year", () => {
    vehicleData.forEach((make) => {
      make.models.forEach((model) => {
        expect(model.years.length).toBeGreaterThan(0);
      });
    });
  });

  it("all model years are in valid range", () => {
    vehicleData.forEach((make) => {
      make.models.forEach((model) => {
        model.years.forEach((year) => {
          expect(year).toBeGreaterThanOrEqual(2015);
          expect(year).toBeLessThanOrEqual(2024);
        });
      });
    });
  });
});
