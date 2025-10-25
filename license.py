import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import axios from 'axios';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { useToast } from '@/components/ui/use-toast';

const LicenseManager = () => {
  const { toast } = useToast();
  const [key, setKey] = useState('');

  // Mock HWID generation (in a real app, use a client-side library or server-generated HWID)
  const hwid = 'mock-hwid-' + Math.random().toString(36).substring(2); // Replace with actual HWID logic

  const validateLicense = useMutation({
    mutationFn: async () => await axios.post('/api/validate-license', { key, hwid }),
    onSuccess: ({ data }) => toast({ title: 'Success', description: data.message }),
    onError: (error: any) => toast({ title: 'Error', description: error.response?.data?.error, variant: 'destructive' }),
  });

  return (
    <Card className="border-void-green bg-void-dark">
      <CardHeader>
        <CardTitle className="text-void-green">License Validation</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          <Input
            value={key}
            onChange={(e) => setKey(e.target.value)}
            placeholder="Enter your license key"
            className="border-void-green bg-void-darker text-foreground"
          />
          <Button
            onClick={() => validateLicense.mutate()}
            className="bg-void-green text-void-dark hover:bg-void-green/80"
            disabled={!key}
          >
            Validate License
          </Button>
        </div>
      </CardContent>
    </Card>
  );
};

export default LicenseManager;
