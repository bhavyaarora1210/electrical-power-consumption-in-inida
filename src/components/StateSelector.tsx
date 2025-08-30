import React from 'react';
import Select from 'react-select';
import { MapPin, Building } from 'lucide-react';

interface StateSelectorProps {
  states: Record<string, string[]> | undefined;
  selectedState: string;
  selectedDistrict: string;
  onStateChange: (state: string) => void;
  onDistrictChange: (district: string) => void;
}

const StateSelector: React.FC<StateSelectorProps> = ({
  states,
  selectedState,
  selectedDistrict,
  onStateChange,
  onDistrictChange,
}) => {
  const stateOptions = states ? Object.keys(states).map(state => ({
    value: state,
    label: state
  })) : [];

  const districtOptions = (states && selectedState) ? 
    states[selectedState].map(district => ({
      value: district,
      label: district
    })) : [];

  const customStyles = {
    control: (provided: any) => ({
      ...provided,
      borderRadius: '0.5rem',
      border: '1px solid #e5e7eb',
      boxShadow: 'none',
      '&:hover': {
        border: '1px solid #3b82f6',
      },
    }),
    option: (provided: any, state: any) => ({
      ...provided,
      backgroundColor: state.isSelected ? '#3b82f6' : 'white',
      color: state.isSelected ? 'white' : '#374151',
      '&:hover': {
        backgroundColor: state.isSelected ? '#3b82f6' : '#f3f4f6',
      },
    }),
  };

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-6">
      <div className="flex items-center space-x-2 mb-4">
        <MapPin className="h-5 w-5 text-blue-600" />
        <h3 className="text-lg font-semibold text-gray-900">Location</h3>
      </div>
      
      <div className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Select State
          </label>
          <Select
            options={stateOptions}
            value={stateOptions.find(option => option.value === selectedState)}
            onChange={(option) => {
              onStateChange(option?.value || '');
              onDistrictChange('');
            }}
            placeholder="Choose a state..."
            styles={customStyles}
            isSearchable
          />
        </div>

        {selectedState && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select District
            </label>
            <Select
              options={districtOptions}
              value={districtOptions.find(option => option.value === selectedDistrict)}
              onChange={(option) => onDistrictChange(option?.value || '')}
              placeholder="Choose a district..."
              styles={customStyles}
              isSearchable
            />
          </div>
        )}
      </div>

      {selectedState && selectedDistrict && (
        <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-100">
          <div className="flex items-center space-x-2 text-blue-800">
            <Building className="h-4 w-4" />
            <span className="text-sm font-medium">
              {selectedDistrict}, {selectedState}
            </span>
          </div>
        </div>
      )}
    </div>
  );
};

export default StateSelector;